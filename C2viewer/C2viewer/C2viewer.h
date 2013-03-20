//
//  C2viewer.h
//  C2viewer
//
//  Created by Bård Fjukstad on 18.03.11.
//  Copyright 2011 Fjukstad Weatherprograms. All rights reserved.
//

#ifndef C2VIEWER_H
#define C2VIEWER_H

//	Includes
#include	<SDL.h>
#include	<stdint.h>
#include	<stdio.h>
#include	<stdlib.h>
#include	<unistd.h>
 

//	Constants
//	Maximum number of images to keep in memory (ie, in decompressed form)
#define	kMax_loaded_images	3
//	Number of frames between each loaded image. More frames means a smoother crossfade.
#define	kMax_sub_frames		10

//	Types
typedef struct { 
	SDL_Surface		*image,			//	Image data after decompression
    *description;	//	A surface with a textual description of the image
	char			*jpg_data;		//	jpeg compressed data
	int				jpg_length;		//	length of jpeg compressed data
	SDL_Rect		size;			//	Size of image
	int				year,			//	Some data about the image.
    month,
    day,
    hour,
    minute;
} img_desc_t; 

//	Prototypes
void	usage(char *name);

//	Image loading
void		load_images(int year, int month, int day);
img_desc_t*	load_image(int year, int month, int day, int hour, int minute);
void		create_image(img_desc_t *img);
void		free_image(img_desc_t *img);

//	Display related
void show_images( img_desc_t *img1, img_desc_t *img2, double framesPrSec);

//	Other stuff
double		current_time(void);

// Cloudiness estimator
double      cloudiness(SDL_Surface	*image);
Uint32      getpixel(SDL_Surface *surface, int x, int y);

#endif
