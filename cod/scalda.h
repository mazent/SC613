#ifndef SCALDA_H_
#define SCALDA_H_

#include "includimi.h"

#define MILLIWATT_1		4700
#define MILLIWATT_2		4700
#define MILLIWATT_3		2700
#define MILLIWATT_4		2900

#define MILLIWATT_X		15000

// Tutto spento dopo ini
bool SCALDA_ini(void) ;

void SCALDA_fin(void) ;

// Controlla le singole resistenze
void SCALDA_1(bool) ;
void SCALDA_2(bool) ;
void SCALDA_3(bool) ;
void SCALDA_4(bool) ;

// Controlla quella globale
void SCALDA_x(bool) ;

#endif
