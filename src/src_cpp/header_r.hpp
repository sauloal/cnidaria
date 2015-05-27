// header_r.hpp
//

#ifndef LZZ_header_r_hpp
#define LZZ_header_r_hpp

#include "rapidjson/document.h"     // rapidjson's DOM-style API
#include "rapidjson/prettywriter.h" // for stringify JSON
#include "rapidjson/filestream.h"   // wrapper of C stream for prettywriter as output
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/filereadstream.h"
#include "rapidjson/encodedstream.h"  

#include "shared.hpp"

namespace cnidaria {
	const static string_t FMT_COMPLETE_BEGIN = "cnidaria/complete/begin";
	const static string_t FMT_COMPLETE       = "cnidaria/complete";
	const static string_t FMT_SUMMARY        = "cnidaria/summary";
	const static string_t FMT_MATRIX         = "cnidaria/matrix";
	const static string_t FMT_JMATRIX        = "cnidaria/json_matrix";
	const static string_t FMT_JELLYFISH      = "binary/sorted";
	
	const static string_t EXT_COMPLETE       = ".cne";
	const static string_t EXT_SUMMARY        = ".cns"; 
	const static string_t EXT_MATRIX         = ".cnm";
	const static string_t EXT_JMATRIX        = ".json";
	const static string_t EXT_JELLYFISH      = ".jf";
}


typedef rapidjson::Document                                json_doc_t;
typedef rapidjson::Value                                   json_val_t;
typedef rapidjson::Document::AllocatorType                 json_allo_t;
typedef rapidjson::StringBuffer                            json_str_buff_t;
typedef rapidjson::SizeType                                json_size_t;
typedef rapidjson::Writer<json_str_buff_t>                 json_writer_fil_t;

#define LZZ_INLINE inline
namespace boost
{
  template <typename B, typename A>
  std::size_t hash_value (boost::dynamic_bitset <B, A> const & bs);
}
namespace cnidaria
{
  bool is_cnidaria (string_t filename);
}
namespace cnidaria
{
  string_t get_file_format (string_t filename);
}
namespace cnidaria
{
  struct j_matrix_s
  {
    baseInt r;
    baseInt c;
    baseint_vec_t columns;
    j_matrix_s ();
    j_matrix_s (baseInt R, baseInt C, baseint_vec_t COL);
  };
}
namespace cnidaria
{
  typedef std::vector <j_matrix_s> j_matrix_s_vec_t;
}
namespace cnidaria
{
  struct header_data
  {
    string_vec_t * infiles;
    string_vec_t * srcfiles;
    tri_baseint_vec_t * matrix;
    hash_table_b_t * hash_table;
    baseint_vec_t * num_kmer_total_spp;
    baseint_vec_t * num_kmer_valid_spp;
    baseInt complete_registers;
    baseInt num_infiles;
    baseInt num_srcfiles;
    baseInt num_combinations;
    baseInt min_val;
    baseInt max_val;
    baseInt save_every;
    baseInt num_pieces;
    baseInt piece_num;
    baseInt kmer_size;
    baseInt kmer_bytes;
    baseInt data_bytes;
    baseInt block_bytes;
    baseInt j_offset;
    baseInt j_size;
    j_matrix_s_vec_t * j_matrices;
    uint_t version;
    string_t filetype;
    header_data ();
    void print ();
    void add (header_data & hda);
    void merge (header_data & hda);
  };
}
namespace cnidaria
{
  class cnidaria_header_r
  {
  protected:
    string_t basename;
    baseInt json_pos;
    std::vector <unsigned char> bytes1;
  public:
    cnidaria_header_r (string_t basenamel = DEFAULT_BASENAME);
    void openfile (std::ifstream & infile_, string_t filename);
    void load (header_data & hda, string_t filename);
    void load (header_data & hda, string_t filename, std::ifstream & infile_);
    void load_complete (header_data & hda, string_t filename);
    void load_complete (header_data & hda, std::ifstream & infile);
    void load_matrix (header_data & hda, string_t filename);
    void load_matrix (header_data & hda, std::ifstream & infile);
    void load_jmatrix (header_data & hda, string_t filename);
    void load_jmatrix (header_data & hda, std::ifstream & infile);
    void load_summary (header_data & hda, string_t filename);
    void load_summary (header_data & hda, std::ifstream & infile);
    void read_json (header_data & hda, std::ifstream & infile, string_t & jsons);
    void read_header (header_data & hda, std::ifstream & infile);
    void parse_header_json (header_data & hda, std::ifstream & infile, string_t & jsonstr);
    void deserialize_matrix (header_data & hda, std::ifstream & infile);
    baseInt get_json_pos ();
  };
}
namespace boost
{
  template <typename B, typename A>
  std::size_t hash_value (boost::dynamic_bitset <B, A> const & bs)
                                                                  {
        return boost::hash_value(bs.m_bits);
  }
}
#undef LZZ_INLINE
#endif
