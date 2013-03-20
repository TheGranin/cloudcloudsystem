//
//  main.c
//  C2viewer
//
//  Created by Bård Fjukstad on 18.03.11.
//  Copyright 2011 Fjukstad Weatherprograms. All rights reserved.
//
//	Includes
#include	<sys/types.h>
#include	<string.h>
#include	<SDL.h>
#include	<SDL_ttf.h>
#include	<SDL_image.h>
#include	<errno.h>
#include	<sys/time.h>  

#include "C2viewer.h"
 
char			*base_path		= "./",		//	The base image path.
*path_storage	= 0;		//	Storage used for generating temporary paths
TTF_Font		*font;						//	Font used for description
SDL_Surface		*screen			= 0;		//	The screen we use to render to
SDL_Surface     *frames_img     = 0;        //  To render speed information
SDL_Rect		scr_rect;					//	Size of the screen
int				base_path_len	= 0;

//  Calclulate "Cloudiness" for region of image.
// Returns "cloudiness" as a percentage of image. If the image is dark, returns 0.0%
// 
double      cloudiness(SDL_Surface	*image){
    // Needs to use sky part of image : box = ( 0, 0 , 626, 266 )
    int x,y;
    Uint8 r,g,b;
    int Nbw = 0;
    int N = 0;  
    int Nbright = 0; 
    Uint32 p;
    double CC;
    
    for (x=0; x<626; x++){
        for (y=0; y<266; y++){
            
            p = getpixel( image, x, y );
            // p is 32 bit unsigned int with the RGB values in 8+8+8 bits
            
            r = p >> 16;
            g = ( p >> 8 ) | 0xFF00;
            b =  p | 0xFF00;
            
            if( ( r + b + g ) > 160 ) Nbright += 1;
            
            if ( b > ( (r + g) / 1.9 ) )  
                Nbw += 1;
            else
                N += 1;
        }
    }
    
    if ( Nbright > ( 626*266 )*0.4 )
        CC = 100.0 - Nbw*100.0/(626*266);
    else
        CC = 0.0;    
    return CC; 
}

//  Getting the Pixel value of one single pixel
Uint32 getpixel(SDL_Surface *surface, int x, int y)
{
    int bpp = surface->format->BytesPerPixel;
    
    /* Here p is the address to the pixel we want to retrieve */
    Uint8 *p = (Uint8 *)surface->pixels + y * surface->pitch + x * bpp;
    
    switch(bpp) {
        case 1:
            return *p;
            break;
            
        case 2:
            return *(Uint16 *)p;
            break;
            
        case 3:
            if(SDL_BYTEORDER == SDL_BIG_ENDIAN)
                return p[0] << 16 | p[1] << 8 | p[2];
            else
                return p[0] | p[1] << 8 | p[2] << 16;
            break;
            
        case 4:
            return *(Uint32 *)p;
            break;
            
        default:
            return 0;       /* shouldn't happen, but avoids warnings */
    }
}

//	load_image: Load a single image, but do not create its SDL_Surface representation
img_desc_t*	load_image(int year, int month, int day, int hour, int minute) {
	img_desc_t	*img;
	FILE		*fd;
	
	//	Create the path
	snprintf(path_storage, base_path_len+1024, "%s/%4d/%02d/%02d/wcam0_%4d%02d%02d_%02d%02d.jpg", base_path, year, month, day, year, month, day, hour, minute);
	fd	= fopen(path_storage, "r");
	if (!fd) {
		//	Couldn't open file. We could deal with this gracefully....
		printf("Failed to open file '%s': %s\n", path_storage, strerror(errno));
		//	...or simply chicken out and exit ;)
		exit(-1);
	}
	img = calloc(1, sizeof(img_desc_t));
	//	Figure out the length of the jpeg file
	fseek(fd, 0, SEEK_END);
	img->jpg_length	= ftell(fd);
	rewind(fd);
	//	Allocate space for jpeg data, and read it
	img->jpg_data	= malloc(img->jpg_length);
	if (fread(img->jpg_data, 1, img->jpg_length, fd) != img->jpg_length) {
		printf("Hmm, we got less data than we were supposed to..\n");
		exit(-1);
	}
	fclose(fd);
	img->year	= year;
	img->month	= month;
	img->day	= day;
	img->hour	= hour;
	img->minute	= minute;
	return img;
}


//	create_image: Create an SDL_Surface for the image in <img>, as well as
//	a descriptor surface using SDL_ttf (if available).
void create_image(img_desc_t *img) {
	SDL_RWops	*rw;
	char		description[128];
	SDL_Color	white	= {255, 255, 255, 0},
    black	= {0, 0, 0, 0};
	SDL_Surface	*image	= 0;
    double cloud = 0.0;
	
	//	Is this image already loaded?
	if (img->image)
		return;
		
	//	Have SDL decode the jpeg data for us
	rw			= SDL_RWFromMem(img->jpg_data, img->jpg_length);
	image		= IMG_LoadTyped_RW(rw, 0, "jpg");
	SDL_FreeRW(rw);
	
	//	Print an error if we didn't manage to load the image.
	if (!image)
		printf("Failed to load image :( %s\n", IMG_GetError());
	else {
		img->size.x	= 0;
		img->size.y	= 0;
		img->size.w	= image->w;
		img->size.h	= image->h;
		
		//	Convert to display format for optimal blitting
		img->image	= SDL_DisplayFormat(image);
		SDL_SetAlpha(img->image, SDL_SRCALPHA, SDL_ALPHA_OPAQUE);
        
        // Add "Cloudiness" to text description
        
        cloud = cloudiness( image );
        
        SDL_FreeSurface(image);
	}
    
	
	//	Create the text description, if we got SDL_TTF to initialize
	if (font) {
		snprintf(description, 128, "%04d-%02d-%02d %02d:%02d    Cloudiness %.1f%%", img->year, img->month, img->day, img->hour, img->minute, cloud);
		//	Text is rendered with white text on black background
		img->description	= TTF_RenderUTF8_Shaded(font, description, white, black);
	}
}

//	free_image: Free resources associated with the passed-in image.
void free_image(img_desc_t *img) {
	if (img) {
		if (img->image)
			SDL_FreeSurface(img->image);
		if (img->description)
			SDL_FreeSurface(img->description);
		if (img->jpg_data)
			free(img->jpg_data);
		
		img->image			= 0;
		img->description	= 0;
		img->jpg_data		= 0;
		free(img);
	}
}

double		current_time(void) {
	struct timeval now;
	gettimeofday(&now, 0);
	return (double)now.tv_sec + (((double)now.tv_usec)/10e6f);
}

// Display images side by side
void show_images( img_desc_t *img1, img_desc_t *img2, double framesPrSec)
{
    
	SDL_Rect	desc_src, desc_dst, img1_dst, img2_dst;
    char		description[128];
    SDL_Color	white	= {255, 255, 255, 0},
    black	= {0, 0, 0, 0};

	
	//	Clear the display. You may want to clear and update only the parts of
	//	the display you intend to update, but that is a performance enhancement
	//	outside the scope of this brief sample.
    
    //	Decode image data for both images
    if (!img1->image)
        create_image(img1);
    
    if (!img2->image)
        create_image(img2);
    
    //	We may not have been able to decode the image data, so double-check
    // that we have an image.
    if( !img1->description && !img1->image )
        return;
    if( !img2->description && !img2->image )
        return;
    
    
    // IMAGE 1
    img1_dst.x			= 0;
    img1_dst.y			= 0;
    img1_dst.w			= 1024/2;
    img1_dst.h			= img1->size.h;
        
    SDL_SetAlpha(img1->image, SDL_SRCALPHA, SDL_ALPHA_OPAQUE);
    SDL_BlitSurface(img1->image, &img1_dst, screen, &img1_dst);
    
    //	Clear old description area (we just clear the entire lower black bar)
    desc_dst.x			= 0;
    desc_dst.y			= img1->size.h;
    desc_dst.w			= 1024/2;
    desc_dst.h			= scr_rect.h-desc_dst.y;
    SDL_FillRect(screen, &desc_dst, 0);
    //	Draw the description
    desc_src.x			= 0;
    desc_src.y			= 0;
    desc_src.w			= 1024/2;
    desc_src.h			= img1->description->h;
    desc_dst.x			= 15;
    desc_dst.y			= img1->size.h+2;
    desc_dst.w			= desc_src.w;
    desc_dst.h			= desc_src.h;
    SDL_BlitSurface(img1->description, &desc_src, screen, &desc_dst);

    // IMAGE 2
    img2_dst.x			= 1024/2;
    img2_dst.y			= 0;
    img2_dst.w			= 1024/2;
    img2_dst.h			= img2->size.h;
        
    SDL_SetAlpha(img2->image, SDL_SRCALPHA, SDL_ALPHA_OPAQUE);
    SDL_BlitSurface(img2->image, &img1_dst, screen, &img2_dst);
    
    //	Clear old description area (we just clear the entire lower black bar)
    desc_dst.x			= 1024/2;
    desc_dst.y			= img2->size.h;
    desc_dst.w			= 1024/2;
    desc_dst.h			= scr_rect.h-desc_dst.y;
    SDL_FillRect(screen, &desc_dst, 0);
    //	Draw the description
    desc_src.x			= 0;
    desc_src.y			= 0;
    desc_src.w			= 1024/2;
    desc_src.h			= img2->description->h;
    desc_dst.x			= 1024/2+15;
    desc_dst.y			= img2->size.h+2;
    desc_dst.w			= desc_src.w;
    desc_dst.h			= desc_src.h;
    SDL_BlitSurface(img2->description, &desc_src, screen, &desc_dst);

    // Add Frames pr Second as displayed information :
	if (font) {
		snprintf(description, 128, "Frames pr second : %.2f", framesPrSec);
		//	Text is rendered with white text on black background
		frames_img	= TTF_RenderUTF8_Shaded(font, description, white, black);
        
        //	Draw the description
        desc_src.x			= 0;
        desc_src.y			= 0;
        desc_src.w			= frames_img->w;
        desc_src.h			= frames_img->h;
        desc_dst.x			= 1024/2 - 80;
        desc_dst.y			= 700;
        desc_dst.w			= desc_src.w;
        desc_dst.h			= desc_src.h;
        SDL_BlitSurface(frames_img, &desc_src, screen, &desc_dst);
        
	}

    // Show doublebuffered screen
    
	SDL_Flip(screen);

}

 
// Run program.
int	main(int argc, char *argv[]) 
{
    SDL_Event			event;
	int					quit	= 0;
	uint8_t				*key_state;
	int					num_keys;
    double              start,now,demo_start_time,sleeptime, framesPrSec=0.0;
    int                 min = 0;
    int                 frames			= 0;		//	Frame counter, used to compute FPS
    
    img_desc_t*         img1 = 0;
    img_desc_t*         img2 = 0;
         
    //	Get length of the base image path, and allocate storage for temporary paths
	base_path_len	= strlen(base_path);
	path_storage	= calloc(1024+base_path_len,1);

	//	Initialize SDL and SDL_ttf
	if (SDL_Init(SDL_INIT_TIMER | SDL_INIT_VIDEO) < 0)
		printf("Failed SDL init! Some things may not work..\n");
    
	if(TTF_Init() == -1)
		printf("Failed to initialize text support: %s\n", TTF_GetError());
	else {
		//	Load font we want to use.
		font	= TTF_OpenFont("./FreeSans.ttf", 18);
		if (!font)
			printf("Failed to open font: %s\n", TTF_GetError());
	}
    
    
    //	Set size of the surface into which we want to draw. You will probably
	//	want to pass the SDL_FULLSCREEN flag to SDL_SetVideoMode below, as well
	//	as use a resolution of 1024x768.
	scr_rect.x	= 0;
	scr_rect.y	= 0;
	scr_rect.w	= 1024;
	scr_rect.h	= 768;
	
	//	Set the video mode. We don't do fullscreen for this sample code
	screen		= SDL_SetVideoMode(scr_rect.w,scr_rect.h, 32, SDL_DOUBLEBUF);

	SDL_FillRect(screen, &scr_rect, 0);
	SDL_WM_SetCaption("Cloudiness Forecast Demonstration",0);
    
    // Load two images in a simple viewer
    // Annotate with "Cloudiness".
    //
    
    // Load images. Params are Year, Month, Day, Hour, Minute
    img1 = load_image(2003, 3, 22, 12, 45);
    img2 = load_image(2003, 3, 22, 16, 45);
    
    if( !img1  && !img2 ) {
        printf("Loaded NULL images.");
        return EXIT_FAILURE;
    }
        
    show_images( img1, img2, framesPrSec );
    
    // Run display loop and wait for user input. Q quits.
    
    demo_start_time	= current_time();
	while (!quit) {
		start	= current_time();
		//	Poll for input events, and handle them.
		while (SDL_PollEvent(&event)) {
			switch (event.type) {
				case SDL_KEYDOWN:
					switch (event.key.keysym.sym) {
						case SDLK_ESCAPE:
						case SDLK_q:
							//	User pressed Q or Escape - time to quit
							quit	= 1;
							break;
						case SDLK_l:
							//	User pressed the "L" key.
							//	Check out SDL/SDK_keysym.h for other keys and their names.
							break;
						default:
							//	Some other key was pressed.
							break;
					}
					break;
				case SDL_QUIT:
					//	SDL wants us to quit. This is event is sent if the user
					//	presses the esc key. (We handle that above as well.)
					quit	= 1;
					break;
				default:
					//	Some other event, like a mouse pointer event, etc.
					break;
			}
		}
        //	Check for keys being continuously pressed. We only get one keydown
		//	event for each key, but the keystate will indicate if the key is
		//	still pressed.
		key_state	= SDL_GetKeyState(&num_keys);
		if (key_state[SDLK_RIGHT]) {
			//	Code to move forwards in time
		}
		if (key_state[SDLK_LEFT]) {
			//	Code to move backwards in time
		}
        

        min += 15;
        if ( min > 50 ) min = 0;
        
        // Load images. Params are Year, Month, Day, Hour, Minute
        free_image(img1);
        free_image(img2);
        
        img1 = load_image(2003, 3, 22, 12, min);
        img2 = load_image(2003, 3, 22, 16, min);
        
        if( !img1  && !img2 ) {
            printf("Loaded NULL images.");
            return EXIT_FAILURE;
        }
        
        show_images( img1, img2, framesPrSec );
		frames++;
		
		//	Print frames per second every five frames
		now	= current_time();
		if (frames % 5) {
            framesPrSec = (double)frames/(now-demo_start_time);
			printf("\rFPS: %.2f   ", framesPrSec);
			fflush(stdout);
		}
		//	Figure out how much we need to sleep, and then sleep a bit.
		if (now-start < 0.033) {
			sleeptime	= (now-start)*1000000;
			usleep(sleeptime);
		}
	}

    
    
    return EXIT_SUCCESS;
}

