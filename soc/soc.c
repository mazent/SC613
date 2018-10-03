#define STAMPA_DBG
#include "includimi.h"
#include "soc.h"

extern void timer_ini(void) ;
extern void timer_run(void) ;
extern bool timer_attivi(void) ;

//// Livello di cpu imposto a compile-time
//#ifdef NDEBUG
//static const RICH_CPU CPU_CT = CPU_FERMA ;
//#else
//// Per debug impedisco deep-sleep
//static const RICH_CPU CPU_CT = CPU_PAUSA ;
//#endif
//
//// Livello di cpu imposto a run-time
//static RICH_CPU cpu_rt = CPU_FERMA ;

typedef struct {
	PF_SOC_APC apc ;
} UNA_APC ;

static UNA_APC vAPC[MAX_SOC_APC] ;


//static void hard_fault(void)
//{
//#ifdef NDEBUG
//	CySoftwareReset() ;
//#else
//	__BKPT(0) ;
//#endif
//}


void SOC_ini(void)
{
//	// sostituisco while(1) con un bel reset
//    (void) CyIntSetSysVector(CY_INT_HARD_FAULT_IRQN, hard_fault) ;

	timer_ini() ;

	for (int i=0 ; i<MAX_SOC_APC ; i++) {
		vAPC[i].apc = NULL ;
	}
}

void SOC_apc(int quale, PF_SOC_APC cb)
{
	ASSERT(quale < MAX_SOC_APC) ;

	if (quale < MAX_SOC_APC)
		vAPC[quale].apc = cb ;
}

void SOC_run(void)
{
	for (int i=0 ; i<MAX_SOC_APC ; i++) {
		PF_SOC_APC apc = vAPC[i].apc ;
		if (apc) {
			vAPC[i].apc = NULL ;
			DBG_PRINTF("eseguo %p\n", apc) ;
			apc() ;
		}
	}

	timer_run() ;
}

//RICH_CPU SOC_cpu(void)
//{
//	RICH_CPU s = MIN(cpu_rt, CPU_CT) ;
//
//	for (int i=0 ; i<MAX_SOC_APC ; i++) {
//		if ( vAPC[i].apc ) {
//			s = CPU_ATTIVA ;
//			break ;
//		}
//	}
//
//	if ( timer_attivi() )
//		s = MIN(CPU_PAUSA, s) ;
//
//	return s ;
//}
//
//void SOC_min(RICH_CPU cpu)
//{
//	cpu_rt = cpu ;
//}

