#ifndef CIRCO_H_
#define CIRCO_H_

#include "includimi.h"

/*
	Per ottenere un buffer circolare di MAX_BUFF elementi:

	Definire

		static union {
			S_CIRCO c ;
			uint8_t b[sizeof(S_CIRCO) - 1 + MAX_BUFF] ;
		} u ;

	Inizializzare con

		CIRCO_iniz(&u.c, MAX_BUFF)

	Successivamente si possono usare le altre funzioni
*/

typedef struct {
	uint16_t DIM_CIRCO ;

	// Inizializzare a 0
	uint16_t leggi ;
	uint16_t tot ;
#ifdef MIN_CIRCO
	uint16_t minLiberi ;
#endif
	uint8_t buf[1] ;
} S_CIRCO ;


void CIRCO_ins(S_CIRCO *, const uint8_t *, uint16_t) ;
uint16_t CIRCO_est(S_CIRCO *, uint8_t *, uint16_t) ;

static inline uint16_t CIRCO_dim(S_CIRCO * x)
{
	return x->tot ;
}

static inline uint16_t CIRCO_liberi(S_CIRCO * x)
{
#ifdef MIN_CIRCO
	uint16_t liberi = x->DIM_CIRCO - x->tot ;
	if (x->minLiberi > liberi) {
		DBG_PRINTF("liberi %d\n", liberi) ;
		x->minLiberi = liberi ;
	}
	return liberi ;
#else
	return x->DIM_CIRCO - x->tot ;
#endif
}

static inline void CIRCO_svuota(S_CIRCO * x)
{
	x->leggi = x->tot = 0 ;
}

static inline void CIRCO_iniz(S_CIRCO * x, uint16_t dim)
{
	x->DIM_CIRCO = dim ;
	x->leggi = x->tot = 0 ;
#ifdef MIN_CIRCO
	x->minLiberi = dim ;
#endif
}

// Test unit
void CIRCO_tu(void) ;

#endif
