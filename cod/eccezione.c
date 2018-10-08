/*
	per avere solo precise fault:

	#define DISDEFWBUF		(1 << 1)
	#define SCB_ACTLR		0xE000E008

	*(uint8_t *) SCB_ACTLR |= DISDEFWBUF ;
*/
#define STAMPA_DBG
#include "includimi.h"

// https://community.arm.com/iot/embedded/f/discussions/3257/debugging-a-cortex-m0-hard-fault

void HardFault_Handler(void)
{
#ifdef NDEBUG
	NVIC_SystemReset() ;
#else
	uint32_t linkreg ;
	uint32_t * hardfaultStack = NULL ;

	__asm volatile( "mov %0, r14" : "=r"(linkreg) );
	switch (linkreg) {
	case 0xFFFFFFF1:
	case 0xFFFFFFF9:
		DBG_PUTS("stack MSP") ;
		hardfaultStack = (uint32_t *) __get_MSP() ;
		break ;
	case 0xFFFFFFFD:
		DBG_PUTS("stack PSP") ;
		hardfaultStack = (uint32_t *) __get_PSP() ;
		break ;
	default:
		DBG_PRINTF("EXC_RETURN ? 0x%08" PRIx32 "?\n", linkreg) ;
		break ;
	}

	if (hardfaultStack) {
		DBG_PRINTF("    %p\n", hardfaultStack) ;
	    DBG_PRINTF("    R0   = 0x%08" PRIx32 "\n", hardfaultStack[0]) ;
	    DBG_PRINTF("    R1   = 0x%08" PRIx32 "\n", hardfaultStack[1]) ;
	    DBG_PRINTF("    R2   = 0x%08" PRIx32 "\n", hardfaultStack[2]) ;
	    DBG_PRINTF("    R3   = 0x%08" PRIx32 "\n", hardfaultStack[3]) ;
	    DBG_PRINTF("    R12  = 0x%08" PRIx32 "\n", hardfaultStack[4]) ;
	    DBG_PRINTF("    LR   = 0x%08" PRIx32 "\n", hardfaultStack[5]) ;
	    DBG_PRINTF("    PC   = 0x%08" PRIx32 "\n", hardfaultStack[6]) ;
	    DBG_PRINTF("    xPSR = 0x%08" PRIx32 "\n", hardfaultStack[7]) ;
	}

	__BKPT(0) ;
#endif
}

