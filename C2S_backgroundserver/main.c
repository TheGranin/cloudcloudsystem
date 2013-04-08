//
//  main.c
//  C2S_backgroundserver
//
//  Created by Bård Fjukstad on 13.03.12.
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

#define ROOTDIR  "/home/shared/wi/"         // Will server data from this directory

static int exit_flag;	                /* Program termination flag	*/

static void signal_handler(int sig_num)
{
	exit_flag = sig_num;
}

/* *************************
 * GET
 * Mongoose http will call this function for each request.
 * May run in separate thread, will be multithreaded.
 *
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
	printf("Uri: %s\n",ri->uri);

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
*/

int main (int argc, const char * argv[])
{
    
	struct mg_context	*ctx; 
		
	(void) signal(SIGTERM, signal_handler);
	(void) signal(SIGINT, signal_handler);
	
	if ((ctx = mg_start()) == NULL) {
		(void) printf("%s\n", "Cannot initialize Mongoose context");
		exit(EXIT_FAILURE);
	}
	
	mg_set_option(ctx, "ports", "9909");	
	mg_set_option(ctx, "max_threads", "10");
	mg_set_option(ctx, "dir_list", "yes");   // Disable directory listing
    mg_set_option(ctx, "root", ROOTDIR );
	
	// mg_set_uri_callback(ctx, "/*", get, NULL);  // Setting callback handler.
	
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

