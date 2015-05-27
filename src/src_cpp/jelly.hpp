// jelly.hpp
//

#ifndef LZZ_jelly_hpp
#define LZZ_jelly_hpp

#include <string>
#include <string.h>

#include <include/jellyfish/mapped_file.hpp>
#include <jellyfish/jellyfish.hpp>

#include "shared.hpp"
#include "header_r.hpp"

namespace jelly {
    const static std::string JELLYFISH_T = "jellyfish";
    const static std::string CNIDARIA_T  = "cnidaria";
    //typedef long long unsigned int             baseInt;
    //typedef unsigned int                       uint_t;
    //typedef std::string                        string_t;
    typedef binary_reader                      j_binary_reader_t;
    typedef jellyfish::file_header             j_file_header_t;
    typedef jellyfish::mapped_file             j_mapped_file_t;
    typedef jellyfish::RectangularBinaryMatrix j_rbm_matrix_t;
    typedef std::auto_ptr<j_rbm_matrix_t>      j_rbm_matrix_ptr_t;
    typedef jellyfish::mer_dna                 j_mer_dna_t;
    typedef j_mer_dna_t                        Key;
}

typedef jelly::j_mer_dna_t                                 j_mer_dna_t;

#define LZZ_INLINE inline
namespace jelly
{
  typedef cnidaria::cnidaria_header_r cnidaria_header;
}
namespace jelly
{
  typedef cnidaria::header_data header_data;
}
namespace jelly
{
  typedef cnidaria::hash_table_b_t hash_table_b_t;
}
namespace jelly
{
  typedef cnidaria::j_matrix_s j_matrix_s;
}
namespace jelly
{
  typedef cnidaria::j_matrix_s_vec_t j_matrix_s_vec_t;
}
namespace jelly
{
  class HeaderFileHolder
  {
  public:
    std::ifstream * in;
    string_t file_arg;
    struct stat st;
    HeaderFileHolder ();
    HeaderFileHolder (string_t file_arg_l);
    void init ();
  };
}
namespace jelly
{
  class jelly_iterator : public HeaderFileHolder
  {
  private:
    baseInt last_id;
    baseInt last_file_coord;
    baseInt final_hash;
    baseInt last_hash;
    bool is_cnidaria;
    bool is_iteratable;
    bool is_valid;
    std::string key;
    baseInt hash;
    baseInt prev_hash;
    CNIDARIA_VAL_TYPE val;
    JELLYFISH_VAL_TYPE tmp_val;
    std::vector <unsigned char> bytes1;
    Key mer;
    j_rbm_matrix_ptr_t jmatrix;
    header_data hda;
    string_vec_t infiles;
    string_vec_t srcfiles;
    tri_baseint_vec_t matrix;
    hash_table_b_t hash_table;
    baseint_vec_t num_kmer_total_spp;
    baseint_vec_t num_kmer_valid_spp;
    j_matrix_s_vec_t j_matrices_s;
  public:
    jelly_iterator ();
    jelly_iterator (string_t const & infile_name);
    string_t gen_key ();
    baseInt gen_hash ();
    baseInt key_to_hash (Key const & key);
    CNIDARIA_VAL_TYPE get_val ();
    CNIDARIA_VAL_TYPE * get_val_ptr ();
    Key get_mer ();
    Key * get_mer_ptr ();
    string_t get_key ();
    string_t * get_key_ptr ();
    void get_mer (Key & m);
    void get_key (string_t & k);
    void get_mer_ptr (Key * m);
    void get_key_ptr (string_t * k);
    baseInt get_hash ();
    bool get_is_iteratable ();
    bool get_is_cnidaria ();
    bool get_is_valid ();
    baseInt get_last_hash ();
    baseInt get_last_id ();
    j_matrix_s_vec_t get_j_matrices ();
    baseInt get_j_size ();
    baseInt get_j_offset ();
    baseInt get_kmer_size ();
    baseInt get_kmer_bits ();
    baseInt get_kmer_bytes ();
    baseInt get_data_bytes ();
    baseInt get_block_bytes ();
    baseInt get_final_hash ();
    baseInt get_mask ();
    baseInt get_num_infiles ();
    baseInt get_num_srcfiles ();
    string_vec_t get_infiles ();
    string_vec_t get_srcfiles ();
    void dump ();
    void gen_last_hash ();
    void print ();
    void jf_to_cnidaria ();
    void gen_j_matrix ();
    bool next (bool binaring = false);
    baseInt goto_coord (baseInt coord);
    void seekHash (baseInt req_hash);
  };
}
#undef LZZ_INLINE
#endif
