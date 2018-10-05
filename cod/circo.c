//#define STAMPA_DBG
#include "main.h"
#include "circo.h"

static uint16_t incr(uint16_t x, uint16_t y, uint16_t l)
{
	x += y ;

	return x % l ;
}

void CIRCO_ins(S_CIRCO * pC, const uint8_t * dati, uint16_t dim)
{
	do {
		if (NULL == pC)
			break ;

		if (NULL == dati)
			break ;

		if (0 == dim)
			break ;

		if (0 == pC->tot)
			pC->leggi = 0 ;

		const uint16_t DIM_CIRCO = pC->DIM_CIRCO ;
		if (dim > DIM_CIRCO) {
			// Non ci staranno mai: copio gli ultimi
			BPOINT ;

			pC->tot = DIM_CIRCO ;
			pC->leggi = 0 ;
			dati += dim - DIM_CIRCO ;
			memcpy(pC->buf, dati, DIM_CIRCO) ;

			// Fatto
			break ;
		}

		const uint16_t LIBERI = DIM_CIRCO - pC->tot ;
		if (dim > LIBERI) {
			// I primi li perdo
			BPOINT ;

			pC->leggi = incr(pC->leggi, dim - LIBERI, DIM_CIRCO) ;

			// Adesso ho spazio: procedo
		}

		// Primo posto dove inserire i nuovi
		uint16_t scrivi = incr(pC->leggi, pC->tot, DIM_CIRCO) ;

		if (1 == dim) {
			pC->buf[scrivi] = *dati ;
			pC->tot++ ;
		}
		else if (pC->leggi >= scrivi) {
			//     s      l
			// ****.......****
			memcpy(pC->buf + scrivi, dati, dim) ;
			pC->tot += dim ;
		}
		else {
			//     l      s
			// ....*******....
			const uint16_t CODA = MINI(dim, DIM_CIRCO - scrivi) ;
			memcpy(pC->buf + scrivi, dati, CODA) ;
			pC->tot += CODA ;

			dim -= CODA ;
			if (dim) {
				memcpy(pC->buf, dati + CODA, dim) ;
				pC->tot += dim ;
			}
		}

	} while (false) ;
}

uint16_t CIRCO_est(S_CIRCO * pC, uint8_t * dati, uint16_t dim)
{
	uint16_t letti = 0 ;

	do {
		if (NULL == pC)
			break ;

		if (NULL == dati)
			break ;

		if (0 == dim)
			break ;

		if (0 == pC->tot)
			break ;

		if (dim > pC->tot)
			dim = pC->tot ;

		if (1 == pC->tot) {
			*dati = pC->buf[pC->leggi] ;
			pC->leggi = incr(pC->leggi, 1, pC->DIM_CIRCO) ;
			pC->tot-- ;
            letti = 1 ;
			break ;
		}

		while (dim) {
			// In un colpo posso leggere o fino alla fine:
			//                l   U
			//     ****.......****
			// o fino al totale:
			//         l      U
			//     ....*******....
			const uint16_t ULTIMO = MINI(pC->DIM_CIRCO, pC->leggi + pC->tot) ;
			const uint16_t DIM = MINI(dim, ULTIMO - pC->leggi) ;
			if (1 == DIM)
				*dati = pC->buf[pC->leggi] ;
			else
				memcpy(dati, pC->buf + pC->leggi, DIM) ;
#ifndef NDEBUG
			memset(pC->buf + pC->leggi, 0xCC, DIM) ;
#endif
			dati += DIM ;
			letti += DIM ;
			pC->tot -= DIM ;

			pC->leggi = incr(pC->leggi, DIM, pC->DIM_CIRCO) ;
			dim -= DIM ;
		}

	} while (false) ;

	return letti ;
}

