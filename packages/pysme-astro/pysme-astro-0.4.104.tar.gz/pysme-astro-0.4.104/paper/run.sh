#!/bin/bash
parallel --bar --joblog parallel.log --header : --results . 'python HD_22049.py {}' ::: log AU_Mic Eps_Eri HN_Peg HD_102195 HD_130322 HD_179949 HD_189733 55_Cnc WASP-18
