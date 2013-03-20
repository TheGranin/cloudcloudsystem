//
//  main.c
//  C3Server
//
//  Created by Bård Fjukstad on 17.03.11.
//  Copyright 2011 Fjukstad Weatherprograms. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
#include <sys/wait.h>
#include <unistd.h>		/* For pause() */
#include <sys/stat.h>

#include "mongoose.h"

#define MAXDATASIZE 4000
#define MAXCHARS 100

static int exit_flag;	                /* Program termination flag	*/
static int helper_num;				/* Answer helper variable */
static int helper1;
static int helper2;
static int helper3;

static int SN1_par;
static int SN2_par;
static int SN3_par;


#define str_eq(s1,s2)  (!strcmp ((s1),(s2)))   /* For easier compares. */
#define strn_eq(s1,s2,n1)  (!strncmp ((s1),(s2),(n1)))   /* For easier compares. */

char *STATUS_PAGE ="<html><body><H1 style=\"text-align:center\">C3 Server reply status</H1>" \
"<table border=\"1\" cellpadding=\"10\" style=\"text-align:center\"> "  \
"<tr> " \
"<th align=\"center\"> Server Frontend 1 </th> " \
"<th align=\"center\"> Server Frontend 2 </th> " \
"<th align=\"center\"> Server Frontend 3 </th> " \
"</tr> " \
"<tr> " \
"<td align=\"center\" style=\"color:red\">%d %% YES </td> " \
"<td align=\"center\" style=\"color:red\">%d %% YES </td> " \
"<td align=\"center\" style=\"color:red\">%d %% YES </td> " \
"</tr></table>" ;

char *FORM_PAGE = "<hr><form action=\"SET_STATUS\" method=\"get\" > " \
"<br/>Server Frontend 1: <input type=\"text\" name=\"S1\" /> %% YES " \
"<br/>Server Frontend 2: <input type=\"text\" name=\"S2\" /> %% YES" \
"<br/>Server Frontend 3: <input type=\"text\" name=\"S3\" /> %% YES" \
"<br><input type=\"submit\" value=\"Set server parameters\" />" \
"</form><hr>" \
"</body></html>";

/* Convert to upper case. */
void strupr( char *str )
{
	char *ptr = NULL;
	
	for(ptr=str;*ptr;ptr++)
	{
		*ptr=toupper(*ptr);
	}
	
}

static void signal_handler(int sig_num)
{
	exit_flag = sig_num;
}

/************************************
 * Parse request: Get server status
 */

void getServerStatus( const char *request) 
{
    char buffr[MAXCHARS] = "";
    char *ptr;
    
    if( strlen(request) > MAXCHARS ) {
        printf("Too long request. Got : %s\n", request);
        return;
    }
    
    strcpy(buffr, request);
    
	ptr = strtok( buffr, "&?");
	    
    while( ptr != NULL ) {
        strupr(ptr);
        
        if( strn_eq(ptr, "S1=", 3)){
            sscanf(ptr+3, "%i",&SN1_par);
        }
        if( strn_eq(ptr, "S2=", 3)){
            sscanf(ptr+3, "%i",&SN2_par);
        }
        if( strn_eq(ptr, "S3=", 3)){
            sscanf(ptr+3, "%i",&SN3_par);
        }
        
        ptr = strtok( NULL, "&?" );
    }
    
    return;
    

}

/***************************
 *  Parse request: Find server number
 */

int getServerNr( const char *request)
{
    char buffr[MAXCHARS] = "";
    char *ptr;
    
    int serverNumber = 0;
    
    if( strlen(request) > MAXCHARS ) {
        printf("Too long request. Got : %s\n", request);
        return (0);
    }

    strcpy(buffr, request);
    
	ptr = strtok( buffr, "&?");
	    
    while( ptr != NULL ) {
        strupr(ptr);
        
        if( strn_eq(ptr, "SERVERNUMBER=", 13)){
            sscanf(ptr+13, "%i",&serverNumber);
            return (serverNumber);
        }

        ptr = strtok( NULL, "&?" );

    }
    
    return (serverNumber);
    
}
/* *************************
 * GET
 * Mongoose http will call this function for each request.
 * May run in separate thread, will be multithreaded.
 */
void get(struct mg_connection *conn, const struct mg_request_info *ri, void *user_data) 
{
	size_t isize;
	size_t size;
	FILE *fp;
	char *data;
	int res;
    int SN;
    int modulus=1;
	
	printf("Request: %s\n",ri->query_string);
	printf("Uri: -->%s<--\n",ri->uri);

    if ( str_eq(ri->uri, "/status.html") ) {
        mg_printf(conn, "HTTP/1.1 200 OK\r\n");
		mg_printf(conn, "Content-Type: text/html\r\n\r\n");
		mg_printf(conn, STATUS_PAGE, SN1_par, SN2_par, SN3_par );
        mg_printf(conn, FORM_PAGE);
        
        return;
    }
    
    if ( str_eq(ri->uri, "/SET_STATUS") ) {
        
        getServerStatus( ri->query_string );
        
        mg_printf(conn, "HTTP/1.1 200 OK\r\n");
		mg_printf(conn, "Content-Type: text/html\r\n\r\n");
		mg_printf(conn, STATUS_PAGE, SN1_par, SN2_par, SN3_par );
        mg_printf(conn, FORM_PAGE);
        
        return;
        
    }
    
	if ( str_eq( ri->uri, "/favicon.ico") ) {
		data  = (char *) malloc( MAXDATASIZE );
		
		struct stat st;
		stat("favicon.ico", &st);
		size = st.st_size;	
		
		fp = fopen("favicon.ico","rb" );
		if (fp == NULL) {
			isize = 0;
			goto finis;			
		} 		
		isize = fread( data, sizeof( char ), size, fp ); 
		
		fclose( fp );
		
	finis:		
		// printf("Sending data if size %d as image \n", (int)size );
		
		mg_printf(conn, "HTTP/1.1 200 OK\r\n");
		mg_printf(conn, "Content-Type: image/png\r\n");
		mg_printf(conn, "Content-Length: %d\r\n\r\n",(int)size );
		
		res = mg_write(conn, data, (int)size);
		return;
		
	}

	if (ri->query_string == NULL) {
		mg_printf(conn, "HTTP/1.1 400 NO DATA RETURNED\r\n");
		mg_printf(conn, "Content-Type: text/plain\r\n\r\n");
		mg_printf(conn, "NULL Query. No answer\r\n");
	    return;
	}
	
	// Else return YES or NO
	//
	
	mg_printf(conn, "HTTP/1.1 200 OK\r\n");
	mg_printf(conn, "Content-Type: text/plain\r\n\r\n");
	helper_num++;
    
    SN = getServerNr(ri->query_string);
    
    SN = SN % 3;  // if someone does not read the assignment correctly
    
    if ( SN == 0 ){
        helper1++;
        if (SN1_par == 0 ) {
            mg_printf(conn, "NO\r\n");				            
        } else if (SN1_par == 100 ) {
            mg_printf(conn, "YES\r\n");				
        } else {
            modulus = 10;
            if ( (helper1 % modulus) <= (SN1_par/10) ) {
                mg_printf(conn, "YES\r\n");				
            } else {
                mg_printf(conn, "NO\r\n");				
            }

        }
    }else if ( SN == 1 ) {
        helper2++;
        if (SN2_par == 0 ) {
            mg_printf(conn, "NO\r\n");				            
        } else if (SN2_par == 100 ) {
            mg_printf(conn, "YES\r\n");				
        } else {
            modulus = 10;
            if ( (helper2 % modulus) <= (SN2_par/10) ) {
                mg_printf(conn, "YES\r\n");				
            } else {
                mg_printf(conn, "NO\r\n");				
            }
            
        }
        
    } else {
        helper3++;
        if (SN3_par == 0 ) {
            mg_printf(conn, "NO\r\n");				            
        } else if (SN3_par == 100 ) {
            mg_printf(conn, "YES\r\n");				
        } else {
            modulus = 10;
            if ( (helper3 % modulus) <= (SN3_par/10) ) {
                mg_printf(conn, "YES\r\n");				
            } else {
                mg_printf(conn, "NO\r\n");				
            }
            
        }
        
    }

	return;
}


int main (int argc, const char * argv[])
{
	helper_num = 0;
    helper1 = 0;
    helper2 = 0;
    helper3 = 0;
    SN1_par = 100;
    SN2_par = 100;
    SN3_par = 100;
    
	struct mg_context	*ctx; 
		
	(void) signal(SIGTERM, signal_handler);
	(void) signal(SIGINT, signal_handler);
	
	if ((ctx = mg_start()) == NULL) {
		(void) printf("%s\n", "Cannot initialize Mongoose context");
		exit(EXIT_FAILURE);
	}
	
	mg_set_option(ctx, "ports", "9909");	
	mg_set_option(ctx, "max_threads", "10");
	mg_set_option(ctx, "dir_list", "no");   // Disable directory listing
	
	mg_set_uri_callback(ctx, "/*", get, NULL);  // Setting callback handler.
	
	printf("Mongoose %s started on port(s) [%s], serving directory [%s]\n",
		   mg_version(),
		   mg_get_option(ctx, "ports"),
		   mg_get_option(ctx, "root"));
	
	fflush(stdout); 
	getchar();
	exit_flag = 9;
	
	(void) printf("Exiting on signal %d, "
				  "waiting for all threads to finish...", exit_flag);
	fflush(stdout);
	mg_stop(ctx);
	
	(void) printf("%s", " done.\n");
	
	return (EXIT_SUCCESS);	
}

