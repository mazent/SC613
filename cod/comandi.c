#define STAMPA_DBG
#include "comandi.h"
#include "ucdc.h"
#include "soc.h"
#include "circo.h"
#include "base64.h"


#define CRC_INI		50707

#define MAX_BUFF		1100

static union {
	S_CIRCO c ;
	uint8_t b[sizeof(S_CIRCO) - 1 + MAX_BUFF] ;
} u ;

static uint8_t rx[100] ;

static uint8_t decod[MAX_BUFF] ;
static size_t dimDec ;

static uint8_t codif[MAX_BUFF] ;
static size_t dimCod ;

static uint8_t tx[1 + MAX_BUFF + 1] ;

static uint8_t checksum(uint8_t * vett, uint16_t dim)
{
	uint8_t cs = 0 ;

	for (uint16_t i=0 ; i<dim ; i++)
		cs += vett[i] ;

	return cs ;
}


static void risposta(uint16_t cmd, void * dati, uint16_t dim)
{
	size_t dimtx = 0 ;

	memcpy(codif, &cmd, sizeof(cmd)) ;
	dimtx += sizeof(cmd) ;

	if (dati) {
		memcpy(codif + dimtx, dati, dim) ;
		dimtx += dim ;
	}

	codif[dimtx] = ~checksum(codif, dimtx) ;
    ++dimtx ;

	dimtx = b64_encode(codif, dimtx, tx + 1) ;

	tx[0] = 0x02 ;
	tx[dimtx + 1] = 0x03 ;
	dimtx += 2 ;
	(void) UCDC_tx(tx, dimtx) ;
}

// Errore nell'esecuzione del comando
#define RSP_ERR 		(1 << 14)
// Errore: richiesta sconosciuta
#define RSP_SCONO 		(2 << 14)
// Ok
#define RSP_OK			(3 << 14)

static void risp_ok(uint16_t cmd, void * dati, uint16_t dim)
{
	cmd |= RSP_OK ;

	risposta(cmd, dati, dim) ;
}

static void risp_scono(uint16_t cmd)
{
	cmd |= RSP_SCONO ;

	risposta(cmd, NULL, 0) ;
}

static void risp_err(uint16_t cmd)
{
	cmd |= RSP_ERR ;

	risposta(cmd, NULL, 0) ;
}


// Lista comandi
#define CMD_ECO		0x0000

static void cmd_exe(void)
{
	uint16_t cmd ;
	uint8_t * dati = decod + 2 ;

	dimDec -= 2 ;

	memcpy(&cmd, decod, 2) ;
	switch (cmd) {
	case CMD_ECO:
		risp_ok(cmd, dati, dimDec) ;
		break ;
	default:
		risp_scono(cmd) ;
		break ;
	}
}

static void cmd_rx(void)
{
	NVIC_DisableIRQ(USB_IRQn) ;
	const uint16_t LETTI = CIRCO_est(&u.c, decod, MAX_BUFF) ;
	NVIC_EnableIRQ(USB_IRQn) ;

	for (size_t i=0 ; i<LETTI ; i++) {
		uint8_t x = decod[i] ;
		switch (x) {
		case 0x02:
			// Inizio
			dimCod = 0 ;
			break ;
		case 0x03:
			// Fine
			dimDec = b64_decode(codif, dimCod, decod) ;

			// Almeno comando e crc
			if (dimDec < 2 + 2) {
				DBG_ERR ;
			}
			else if (0xFF == checksum(decod, dimDec)) {
				// Valido!
				dimDec -= 1 ;
				SOC_apc(APC_CMD_EXE, cmd_exe) ;
			}
			else {
				DBG_ERR ;
			}
			break ;
		default:
			if (dimCod < MAX_BUFF)
				codif[dimCod++] = x ;
			break ;
		}
	}
}


// Dentro ISR
static void cdc_rx(void * v, uint16_t d)
{
	CIRCO_ins(&u.c, (const uint8_t *) v, d) ;

	SOC_apc(APC_CMD_RX, cmd_rx) ;

	UCDC_rx(rx, sizeof(rx)) ;
}

static void cdc_ini(void)
{
	UCDC_rx(rx, sizeof(rx)) ;
}

static void cdc_tx(void)
{
	// Non mi serve
}

static const UCDC_CFG cdc = {
	.cb_rx = cdc_rx,
	.cb_tx = cdc_tx,
	.cb_ini = cdc_ini
};

bool CMD_ini(void)
{
	CIRCO_iniz(&u.c, MAX_BUFF) ;

    return UCDC_ini(&cdc) ;
}
