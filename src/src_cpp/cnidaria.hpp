// cnidaria.hpp
//

#ifndef LZZ_cnidaria_hpp
#define LZZ_cnidaria_hpp

//gprof tree > gmon.out.txt
//http://jovislab.com/blog/?p=89

#include <algorithm>
#include <errno.h>
#include <clocale>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <functional>
#include <getopt.h>
#include <iostream>
#include <math.h>
#include <sstream>
#include <stdint.h>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <thread>         // std::thread
#include <unistd.h>
#include <vector>
#include <sys/stat.h>

#include <omp.h>

#include "progressbar.hpp"
#include "shared.hpp"
#include "header_r.hpp"
#include "jelly.hpp"
#include "header_w.hpp"
#include "cnidaria_methods.hpp"

#define LZZ_INLINE inline
int fact (int n);
void version ();
namespace cnidaria
{
  void openoutfile (std::ofstream & outfile_, string_t filename);
}
namespace cnidaria
{
  void openinfile (std::ifstream & infile_, string_t filename);
}
namespace cnidaria
{
  void merge_complete (string_t out_file, string_vec_t cfiles);
}
namespace cnidaria
{
  void merge_complete_parallel (string_t out_file, string_vec_t cfiles, baseInt num_threads = 5);
}
namespace cnidaria
{
  void merge_complete_parallel_piece (string_t out_file, baseInt numCFiles, baseInt fileCount, pos_type begin_pos, string_t infile);
}
namespace cnidaria
{
  void merge_matrix (string_t out_file, string_vec_t cfiles);
}
namespace cnidaria
{
  void merge_matrixj (string_t out_file, string_vec_t cfiles);
}
namespace cnidaria
{
  struct piece_data
  {
    string_vec_t srcfiles;
    string_t out_file;
    baseInt num_threads;
    baseInt minVal;
    baseInt save_every;
    bool export_complete;
    bool export_summary;
    bool export_matrix;
    baseInt num_pieces;
    baseInt piece_num;
    merge_jfs * merger;
    boost::recursive_mutex * locker;
    piece_data (string_vec_t & srcfiles_, string_t & out_file_, baseInt num_threads_, baseInt minVal_, baseInt save_every_, bool export_complete_, bool export_summary_, bool export_matrix_, baseInt num_pieces_, baseInt piece_num_);
  };
}
namespace cnidaria
{
  typedef std::vector <piece_data> piece_data_vec_t;
}
namespace cnidaria
{
  void send_pieces (piece_data_vec_t data);
}
namespace cnidaria
{
  void send_piece (piece_data data);
}
namespace cnidaria
{
  void send_data (string_vec_t srcfiles, string_t out_file, baseInt num_threads, baseInt minVal, baseInt save_every, bool export_complete, bool export_summary, bool export_matrix, baseInt num_pieces, baseInt piece_num);
}
namespace cnidaria
{
  void merge_data (string_t out_file, string_vec_t srcfiles_complete, string_vec_t srcfiles_matrix, string_vec_t srcfiles_matrixj, bool do_merge_complete, bool do_merge_matrix);
}
namespace cnidaria
{
  void dump (string_vec_t infiles);
}
namespace cnidaria
{
  void dump (string_t infile);
}
#undef LZZ_INLINE
#endif
