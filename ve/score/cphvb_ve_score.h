/*
 * Copyright 2011 Mads R. B. Kristensen <madsbk@gmail.com>
 *
 * This file is part of cphVB <http://code.google.com/p/cphvb/>.
 *
 * cphVB is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * cphVB is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with cphVB. If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __CPHVB_VE_SCORE_H
#define __CPHVB_VE_SCORE_H

#include <cphvb.h>

#ifdef __cplusplus
extern "C" {
#endif

cphvb_com *myself = NULL;
cphvb_userfunc_impl reduce_impl = NULL;
cphvb_intp reduce_impl_id = 0;
cphvb_userfunc_impl random_impl = NULL;
cphvb_intp random_impl_id = 0;

cphvb_error cphvb_ve_score_init(

    cphvb_com       *self

);

cphvb_error cphvb_ve_score_execute(cphvb_intp instruction_count,
                                   cphvb_instruction* instruction_list);

cphvb_error cphvb_ve_score_shutdown(void);

cphvb_error cphvb_ve_score_reg_func(char *lib, char *fun, cphvb_intp *id);

//Implementation of the user-defined funtion "reduce". Note that we
//follows the function signature defined by cphvb_userfunc_impl.
cphvb_error cphvb_reduce(cphvb_userfunc *arg);

#ifdef __cplusplus
}
#endif

#endif
