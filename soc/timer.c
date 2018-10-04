//#define STAMPA_DBG
#include "includimi.h"
#include "soc.h"

// Evita di svegliare inutilmente da sleep
#define DISAB_TICK		1

/*
 * Il valore di un timer e' composto da:
 * 		1		  servito
 * 		 1		  scaduto
 * 		  ....... durata
 *
 * La durata vale (TS_SCADUTO - numero-tick)
 * Man mano che vengono contati i tick, la durata
 * aumenta fino a TS_SCADUTO
 */

static const uint32_t TS_SERVITO = 1 << 31 ;
static const uint32_t TS_SCADUTO = 1 << 30 ;

static volatile bool tick ;
static bool tick_attivo ;


typedef struct {
	uint32_t val ;
	PF_TIMER_SW cb ;
} UN_TIMER ;

static UN_TIMER lista_timer[MAX_TIMER_SW] ;

//static void tick_isr(void)
//{
//	tick = true ;
//
//	DPM_tick() ;
//}

void HAL_SYSTICK_Callback(void)
{
	tick = true ;
}

void timer_setcb(int quale, PF_TIMER_SW cb)
{
	ASSERT(quale < MAX_TIMER_SW) ;

	if (quale < MAX_TIMER_SW)
		lista_timer[quale].cb = cb ;
}


void timer_start(int quale, uint32_t ms)
{
	ASSERT(quale < MAX_TIMER_SW) ;
	ASSERT(ms) ;

	if (0 == ms) {
	}
	else if (quale >= MAX_TIMER_SW) {
	}
	else {
#ifdef MILLI_PER_TICK
		// Arrotondo
		uint32_t tick = (ms + MILLI_PER_TICK - 1) / MILLI_PER_TICK ;
#else
		uint32_t tick = ms ;
#endif
		if (tick > TS_SCADUTO)
			tick = TS_SCADUTO ;

		lista_timer[quale].val = TS_SCADUTO - tick ;
#ifdef DISAB_TICK
		if (!tick_attivo) {
			DBG_PUTS("Abilito tick") ;
			SysTick->VAL   = 0UL;                                             /* Load the SysTick Counter Value */
			SysTick->CTRL  = SysTick_CTRL_CLKSOURCE_Msk |
					SysTick_CTRL_TICKINT_Msk   |
					SysTick_CTRL_ENABLE_Msk;                         /* Enable SysTick IRQ and SysTick Timer */
			tick_attivo = true ;
		}
#endif
	}
}

void timer_stop(int quale)
{
	ASSERT(quale < MAX_TIMER_SW) ;

	if (quale < MAX_TIMER_SW)
		lista_timer[quale].val = TS_SERVITO ;
}

bool timer_running(int quale)
{
	bool esito = false ;

	ASSERT(quale < MAX_TIMER_SW) ;

	if (quale < MAX_TIMER_SW)
		esito = lista_timer[quale].val != TS_SERVITO ;

	return esito ;
}

// La prima funzione da invocare

void timer_ini(void)
{
    for (int t = 0 ; t < MAX_TIMER_SW ; t++) {
    	lista_timer[t].val = TS_SERVITO ;
    	lista_timer[t].cb = NULL ;
    }

//	// Inizializzo (tick = 1ms)
//	CySysTickStart() ;
//
//	// Fermo e modifico
//	CySysTickStop() ;
//
//	// Comunque uso il mio
//	(void) CyIntSetSysVector(CY_INT_SYSTICK_IRQN, tick_isr) ;

    /**Configure the Systick interrupt time */
    uint32_t x = HAL_RCC_GetHCLKFreq() / 1000 ;
    x *= MILLI_PER_TICK ;
    HAL_SYSTICK_Config(x) ;

    /**Configure the Systick */
    HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK) ;

    /* SysTick_IRQn interrupt configuration */
    HAL_NVIC_SetPriority(SysTick_IRQn, 0, 0) ;

	// L'interruzione non e' scattata
	tick = false ;

#ifdef DISAB_TICK
	// Per ora non mi serve il tick
	tick_attivo = false ;
	SysTick->CTRL &= ~SysTick_CTRL_ENABLE_Msk ;
#else
	tick_attivo = true ;
#endif
}

// Invocare periodicamente

void timer_run(void)
{
	if (tick) {
		tick = false ;

		// Aggiorno
		for (int t = 0 ; t < MAX_TIMER_SW ; t++) {
			if (lista_timer[t].val != TS_SERVITO)
				lista_timer[t].val++ ;
		}

		// Eseguo
		for (int t = 0 ; t < MAX_TIMER_SW ; t++) {
			if (TS_SCADUTO == lista_timer[t].val) {
				lista_timer[t].val = TS_SERVITO ;

				if (lista_timer[t].cb) {
					DBG_PRINTF("eseguo timer %d\n", t) ;
					lista_timer[t].cb() ;
				}
			}
		}
#ifdef DISAB_TICK
		// E adesso?
		int conta = 0 ;
		for (int t = 0 ; t < MAX_TIMER_SW ; t++) {
			if (lista_timer[t].val != TS_SERVITO)
				conta++ ;
		}
		if (0 == conta) {
			DBG_PUTS("Disabilito tick") ;
			SysTick->CTRL &= ~SysTick_CTRL_ENABLE_Msk ;
			tick_attivo = false ;
		}
#endif
	}
}

bool timer_attivi(void)
{
#ifdef DISAB_TICK
	return tick_attivo || tick ;
#else
	bool attivi = false ;

	for (int t = 0 ; t < MAX_TIMER_SW ; t++) {
		if (lista_timer[t].val != TS_SERVITO) {
			attivi = true ;
			break ;
		}
	}

	return attivi ;
#endif
}
