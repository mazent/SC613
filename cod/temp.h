#ifndef TEMP_H_
#define TEMP_H_

#include "includimi.h"

bool TEMP_iniz(void) ;
void TEMP_fine(void) ;

// Temperature in centesimi di grado
typedef struct {
	// esterne
	int16_t temp1 ;
	int16_t temp2 ;
	int16_t temp3 ;
	int16_t temp4 ;
	// interna
	int16_t temp ;
} S_TEMP ;

bool TEMP_val(S_TEMP *) ;

#endif
