#ifndef __PROGRESS_BAR_HPP__
#define __PROGRESS_BAR_HPP__

#include <iostream>
#include <stdint.h>
#include <stdio.h>
#include <locale>
#include <locale.h>
#include <string.h>
#include <stdlib.h>

//#define PROGRESS_BAR_SHOW_SECS

class progressBar {
  typedef unsigned long long int baseInt;
  
  private:
	std::string name;
	baseInt     minValue;
	baseInt     maxValue;
	baseInt     lastPercent;
	baseInt     lastValue;
	baseInt     lastPos;
	baseInt     diff;
	baseInt     percent;
	baseInt     pos;
	bool        progress;
	bool        two_lines;
	bool        show_secs;
	time_t      startTime;
  public:
	progressBar() {};
	
	progressBar( std::string namel, baseInt minValuel, baseInt maxValuel ):
		name(namel)      , minValue(minValuel), maxValue(maxValuel), lastPercent(9999), lastValue(0)   , lastPos(0),
		diff(0)          , percent(0)         , pos(0)             , progress(true)   , two_lines(true), show_secs(false) {

	  updateStartTime();
	  diff      = maxValue - minValue;

	  std::setlocale(LC_ALL,"");
	}
	
	void updateStartTime()     { startTime = time(NULL); }
	void setProgress( bool p ) { progress  = p;          }
	void setTwoLines( bool t ) { two_lines = t;          }
	void setShowSecs( bool s ) { show_secs = s;          }
	
	void sec_to_str(char * str, baseInt  secs){
	  int secsDay,secsHour,secsMin,secsSec;

	  secsDay  = secs / (3600.0 * 24);
	  secs     = secs % (3600   * 24);
	  secsHour = secs /  3600.0;
	  secs     = secs %  3600;
	  secsMin  = secs /    60.0;
	  secs     = secs %    60;

	  secsSec  = secs;

	  if ( secsDay > 9 ) { secsDay = 9; }

	  if ( show_secs   ) {
		sprintf( str, "%1d.%02d:%02d:%02d", secsDay, secsHour, secsMin, secsSec );
	  } else {
		sprintf( str, "%1d.%02d:%02d"  , secsDay, secsHour, secsMin );
	  }
	}
	
	void set_name( std::string namel ) {
	  name = namel;
	}
	
	inline bool isvalid( baseInt current ) {
	  if ( current != lastValue ) {
		
		lastValue = current;
	  
		if ( current < minValue ) {
		     current = minValue + 1;
		}
		
		pos     = current - minValue;
		
		if ( pos != lastPos ) {
		  lastPos = pos;
		  
		  percent = ( (double)(pos) / (double)diff ) * 1000.0;
		  
		  //std::cout << "curr " << current << " pos " << pos << " min " << minValue << " max " << maxValue << " diff " << diff << " perc " << percent << " last perc " << lastPercent << std::endl;
		  
		  if ( percent != lastPercent ) {
			lastPercent = percent;
			return true;
		  } else {
			return false;
		  }
		} else {
		  return false;
		}
	  } else {
		return false;
	  }
	}


	inline bool print( baseInt current ) {
	  //std::cout << "curr " << current << " pos " << pos << " min " << minValue << " max " << maxValue << " diff " << diff << " perc " << percent << " last perc " << lastPercent << std::endl;
	  bool v = isvalid( current );
	  
	  if ( v ) {
		std::string bar;

		time_t      ela     = difftime( time(NULL), startTime );
		double      speed   = (double)pos  / (ela+1);
		baseInt     missing = diff - pos;
		
		if ( pos    > diff ) { missing = 1; }
		if ( speed == 0.0  ) { speed   = 1; }
		
		char       elaStr[15];
		sec_to_str(elaStr, ela);


		if ( progress ) {
		  double etc           = (double)missing / speed;
		  
		  double percent_print = (double)percent / 10.0;
		  
		  if ( percent_print > 100.0 ) {
			percent_print = 101.0;
		  }
		
		  for ( int i = 0; i < 100; i++ ){
			if( i < (int)percent_print ){
			  bar.replace( i,1,"=" );
			}else if( i == (int)percent_print ){
			  bar.replace( i,1,">" );
			}else{
			  bar.replace( i,1," " );
			}
		  }
	  
		  //std::cout << "\r" <<  << "[" << bar << "] ";
		  //std::cout.width( 6 );
  
		  char       etcStr[15];
		  sec_to_str(etcStr, etc);

		  if ( two_lines ) {
		    std::fprintf( stdout, "%s [%s] %6.1lf%%\n", name.c_str(), bar.c_str(), percent_print );
			//std::fprintf( stdout, "%s kmers: done %'13llu total %'13llu left %'13llu | time: ela %s etc %s | speed %'8llu kmer/s\n\n",
			std::fprintf( stdout, "%s kmers: done %'13llu total %'13llu left %'13llu | time: ela %s etc %s | speed %'10.0f kmer/s\n",
					  name.c_str(), pos, diff, missing, elaStr, etcStr, speed);
		  } else {
			//std::fprintf( stdout, "%s kmers: done %'13llu total %'13llu left %'13llu | time: ela %s etc %s | speed %'8llu kmer/s\n\n",
			std::fprintf( stdout, "%s kms: done %'13llu total %'13llu left %'13llu | t: ela %s etc %s | s %'10.0f km/s | %5.1lf%%\n",
					  name.c_str(), pos, diff, missing, elaStr, etcStr, speed, percent_print);
		  }

		} else {
		  //std::fprintf( stdout, "%s kmers: done %'13llu                                        | time: ela %s                | speed %'8llu kmer/s\n\n",
		  std::fprintf( stdout, "%s kmers: done %'13llu                                        | time: ela %s             | speed %'10.0f kmer/s\n",
					  name.c_str(), pos, elaStr, speed);
		}
		
		std::cout.flush();
	  }
	  
	  return v;
	}
};

#endif