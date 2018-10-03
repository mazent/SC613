#ifndef SOC_H_
#define SOC_H_

/*
 * Sistema operativo cooperativo
 */

#include "includimi.h"

#include "soc_cfg.h"

// Altri pezzi di soc
#include "timer.h"

void SOC_ini(void) ;

typedef void (* PF_SOC_APC)(void) ;

void SOC_apc(int, PF_SOC_APC) ;


void SOC_run(void) ;

//RICH_CPU SOC_cpu(void) ;
//
//void SOC_min(RICH_CPU) ;

#endif
