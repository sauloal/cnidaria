#ifndef __SHARED_HEADER_HPP__
#define __SHARED_HEADER_HPP__


#ifndef __CNIDARIA_VERSION__
#define __CNIDARIA_VERSION__ 8
#endif

#ifndef DEFAULT_BASENAME
#define DEFAULT_BASENAME "cnidaria_db"
#endif

//#ifndef JSON_SIZE_COMPLETE
//#define JSON_SIZE_COMPLETE 51200
//#endif

#ifndef DEFAULT_MIN_NUMBER_SPP_PERC
#define DEFAULT_MIN_NUMBER_SPP_PERC 0.0
#endif

#ifndef DEFAULT_MAX_NUMBER_SPP_PERC
#define DEFAULT_MAX_NUMBER_SPP_PERC 1.0
#endif

#ifndef DEFAULT_MAX_DB_SIZE_EXPONENT
#define DEFAULT_MAX_DB_SIZE_EXPONENT 31
#endif

//#define EXPAND_OUT_BUFFER
#ifdef EXPAND_OUT_BUFFER
#define COMPLETE_OUT_BUFFER_SIZE 65536
#endif

#include <cstring>
#include <string>
#include <string.h>

#include <stdint.h>
#include <time.h>  // NOLINT

#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <sstream>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>

#define BOOST_DYNAMIC_BITSET_DONT_USE_FRIENDS
#include <boost/dynamic_bitset.hpp>


#include <boost/atomic.hpp>
#include <boost/config.hpp> 
#include <boost/format.hpp> 
#include <boost/thread.hpp>
#include <boost/unordered_map.hpp>
#include <boost/functional/hash.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/make_shared.hpp>

#include "boost/threadpool.hpp"



typedef long long unsigned int                baseInt;
//typedef uint64_t                              baseInt;

typedef double                                baseFloat;

typedef unsigned int                          uint_t;
typedef const char*                           const_char_str_t;
typedef char*                                 char_str_t;
typedef std::string                           string_t;
typedef std::char_traits<char>::pos_type      pos_type;

typedef std::vector<const char *>             const_char_vec_t;
typedef std::vector<char *>                   char_vec_t;
typedef std::vector<uint64_t>                 uint64_vec_t;
typedef std::vector<uint8_t>                  uint8_vec_t;
typedef std::vector<bool>                     bool_vec_t;
typedef std::vector<string_t>                 string_vec_t;

typedef std::vector<baseInt  >                baseint_vec_t;
typedef std::vector<baseFloat>                basefloat_vec_t;
typedef std::vector<baseint_vec_t >           bi_baseint_vec_t;
typedef std::vector<basefloat_vec_t >         bi_basefloat_vec_t;
typedef std::vector<bi_baseint_vec_t >        tri_baseint_vec_t;
typedef std::map <string_t, basefloat_vec_t > dbMap;

typedef boost::dynamic_bitset<unsigned char>        b_bitset_t;


#define JELLYFISH_VAL_TYPE  uint64_t
#define CNIDARIA_VAL_TYPE   b_bitset_t

struct intPair {
  baseInt val1;
  baseInt val2;
};

typedef std::vector<intPair>                  intPair_vec_t;


namespace cnidaria {
  //typedef baseInt                                            baseInt;

  //typedef boost::dynamic_bitset<unsigned char>        b_bitset_t;
  typedef boost::threadpool::pool                            b_pool_t;
  
  typedef boost::unordered_map< CNIDARIA_VAL_TYPE, baseInt > hash_table_b_t;
}


#endif