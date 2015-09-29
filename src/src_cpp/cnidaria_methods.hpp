// cnidaria_methods.hpp
//

#ifndef LZZ_cnidaria_methods_hpp
#define LZZ_cnidaria_methods_hpp

#include <thread>         // std::thread

#include "progressbar.hpp"
#include "shared.hpp"
#include "header_r.hpp"
#include "jelly.hpp"
#include "header_w.hpp"

#define LZZ_INLINE inline
namespace cnidaria
{
  baseInt get_max_threads ();
}
namespace cnidaria
{
  class cnidaria_db
  {
  public:
    string_vec_t infiles;
    string_vec_t srcfiles;
    string_t basename;
    double min_val_d;
    double max_val_d;
    baseInt min_val_i;
    baseInt max_val_i;
    bool export_complete;
    bool export_summary;
    bool export_matrix;
    baseInt complete_registers;
    baseInt num_infiles;
    baseInt num_srcfiles;
    std::ofstream * ext_outfile_;
    baseInt j_offset;
    baseInt j_size;
    j_matrix_s_vec_t j_matrices;
    baseint_vec_t num_kmer_total_spp;
    baseint_vec_t num_kmer_valid_spp;
    tri_baseint_vec_t matrix;
    hash_table_b_t hash_table;
    cnidaria_header_rw hd;
    cnidaria_db ();
    cnidaria_db (string_vec_t & srcfilesl, string_t basenamel = DEFAULT_BASENAME);
    void set_min_val (double mi);
    void set_max_val (double ma);
    void set_min_val (baseInt mi);
    void set_max_val (baseInt ma);
    void set_complete_registers (baseInt cr);
    baseInt get_complete_registers ();
    void set_export_summary (bool s);
    void set_export_matrix (bool s);
    void set_export_complete (header_data & hda, bool s, string_t filename = "");
    void enable_summary ();
    void disable_summary ();
    void enable_matrix ();
    void disable_matrix ();
    void disable_complete ();
    void enable_complete (header_data & hda, string_t filename = "");
    void close_complete (header_data & hda);
    void amendHeaderData (header_data & hda);
    void save_all (header_data & hda, string_t filename = "");
    void load_all (header_data & hda, string_t filename = "");
    void load (header_data & hda, string_t filename = "");
    void save_summary (header_data & hda, string_t filename = "");
    void load_summary (header_data & hda, string_t filename = "");
    void save_matrix (header_data & hda, string_t filename = "");
    void save_json_matrix (header_data & hda, string_t filename = "");
    void load_matrix (header_data & hda, string_t filename = "");
    void serialize_complete_register (header_data & hda, register_data d);
    void merge (cnidaria_db & data);
    void add (CNIDARIA_VAL_TYPE & resb, baseInt & numValid);
  };
}
namespace cnidaria
{
  class heapdata
  {
  private:
    typedef jelly::jelly_iterator j_file_iterator_t;
    string_t name;
    bool valid;
    baseInt kmers;
    j_file_iterator_t * it;
  public:
    heapdata ();
    heapdata (string_t const & n);
    void print ();
    bool next ();
    void seekHash (uint64_t req_hash);
    string_t const get_name ();
    bool const get_valid ();
    baseInt const get_kmers ();
    string_t const get_key ();
    string_t * get_key_ptr ();
    j_mer_dna_t const get_mer ();
    j_mer_dna_t * get_mer_ptr ();
    CNIDARIA_VAL_TYPE const get_val ();
    CNIDARIA_VAL_TYPE * get_val_ptr ();
    j_matrix_s_vec_t const get_j_matrices ();
    baseInt const get_j_size ();
    baseInt const get_j_offset ();
    string_vec_t const get_infiles ();
    string_vec_t const get_srcfiles ();
    baseInt const get_kmer_size ();
    baseInt const get_kmer_bytes ();
    baseInt const get_data_bytes ();
    baseInt const get_block_bytes ();
    baseInt const get_final_hash ();
    baseInt const get_hash ();
    baseInt const get_last_hash ();
    baseInt const get_num_srcfiles ();
    baseInt const get_num_infiles ();
    void set_valid (bool v);
  };
}
namespace cnidaria
{
  class jfheap
  {
    typedef std::vector <heapdata*> heap_vec_t;
  public:
    baseInt minH;
    baseInt lminH;
    baseInt numValid;
    baseInt num_infiles;
    baseInt num_srcfiles;
    baseInt minValid;
    baseInt num_pieces;
    baseInt piece_num;
    baseInt piecehash;
    baseInt beginhash;
    baseInt endhash;
    baseInt finalhash;
    baseInt lasthash;
    baseInt tmp_offset;
    baseInt tmp_num_infiles;
    string_t name;
    CNIDARIA_VAL_TYPE resb;
    CNIDARIA_VAL_TYPE rest;
    string_t minKey;
    j_mer_dna_t minMer;
    CNIDARIA_VAL_TYPE tmp_res;
    cnidaria_db * hash_table;
    heap_vec_t data;
    jfheap ();
    jfheap (cnidaria_db & hash_tableL);
    jfheap (cnidaria_db & hash_tableL, baseInt num_piecesl, baseInt piece_numl, string_t namel);
    j_matrix_s_vec_t get_j_matrices ();
    baseInt get_begin_hash ();
    baseInt get_end_hash ();
    baseInt get_last_hash ();
    baseInt get_j_size ();
    baseInt get_j_offset ();
    baseInt get_kmer_size ();
    baseInt get_kmer_bytes ();
    baseInt get_final_hash ();
    baseInt get_block_bytes_in ();
    baseInt get_data_bytes_in ();
    baseInt get_block_bytes_out ();
    baseInt get_data_bytes_out ();
    string_vec_t get_srcfiles ();
    string_vec_t get_infiles ();
    void setMinValid (baseInt minValidl);
    void init ();
    bool next ();
    bool next (CNIDARIA_VAL_TYPE & r, baseInt & valid);
    void get (CNIDARIA_VAL_TYPE & r, baseInt & valid);
    void getVec (CNIDARIA_VAL_TYPE & r);
    baseInt getValid ();
    void update ();
    void seekHash (uint64_t req_hash);
  };
}
namespace cnidaria
{
  class merge_jfs
  {
  public:
    string_vec_t srcfiles;
    string_t basename;
    baseInt num_threads;
    baseInt num_pieces;
    baseInt piece_num;
    baseInt save_every;
    baseInt dump_every;
    baseInt gCounter;
    baseInt num_srcfiles;
    baseInt kmer_size;
    baseInt kmer_bytes;
    baseInt data_bytes;
    baseInt block_bytes;
    bool export_complete;
    bool export_summary;
    bool export_matrix;
    cnidaria_db hash_table;
    header_data hda;
    progressBar progressD;
    progressBar progressG;
    static progressBar progressS;
    static baseInt sCounter;
    merge_jfs (string_vec_t & srcfilesl, string_t basenamel = "cnidaria_db");
    void init ();
    baseInt get_complete_registers ();
    void set_save_every (baseInt pe);
    void set_num_pieces (baseInt np);
    void set_piece_num (baseInt pn);
    void set_min_val (double mi);
    void set_max_val (double ma);
    void set_min_val (baseInt mi);
    void set_max_val (baseInt ma);
    void set_complete_registers (baseInt cr);
    void append_complete_registers (baseInt cr);
    void set_export_summary (bool s);
    void set_export_matrix (bool s);
    void set_export_complete (bool s, string_t filename = "");
    void enable_summary ();
    void enable_matrix ();
    void disable_summary ();
    void disable_matrix ();
    void disable_complete ();
    void enable_complete (string_t filename = "");
    void save_all (string_t filename = "");
    void load_all (string_t filename = "");
    void load (string_t filename = "");
    void save_summary (string_t filename = "");
    void load_summary (string_t filename = "");
    void save_matrix (string_t filename = "");
    void save_json_matrix (string_t filename = "");
    void load_matrix (string_t filename = "");
    void close_complete ();
    void set_num_threads (baseInt nt);
    void updateHeaderData ();
    void run (boost::recursive_mutex * g_guard_s = NULL);
    void run_process (baseInt const thread_num, boost::recursive_mutex * g_guard_s, boost::recursive_mutex * g_guard_m, boost::recursive_mutex * g_guard_e);
    void merge (merge_jfs & merger);
    void merge (merge_jfs * merger);
  };
}
#undef LZZ_INLINE
#endif
