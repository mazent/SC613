#ifndef UCDC_H_
#define UCDC_H_

/*
 * USB device CDC
 */

#include "includimi.h"

typedef void (* PF_UCDC_INI_CB)(void) ;
typedef void (* PF_UCDC_RX_CB)(void *, uint16_t) ;
typedef void (* PF_UCDC_TX_CB)(void) ;

typedef struct {
	// in questa conviene invocare UCDC_rx
	PF_UCDC_INI_CB cb_ini ;

	// anche in questa
	PF_UCDC_RX_CB cb_rx ;

	PF_UCDC_TX_CB cb_tx ;
} UCDC_CFG ;


bool UCDC_ini(const UCDC_CFG *) ;

// inizia la trasmissione, alla fine viene invocata cb_tx
bool UCDC_tx(void *, uint16_t) ;

// inizia la ricezione, quando arriva viene invocata cb_rx
void UCDC_rx(void *, uint16_t) ;

#endif

