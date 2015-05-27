// header_w.hpp
//

#ifndef LZZ_header_w_hpp
#define LZZ_header_w_hpp

#include "progressbar.hpp"
#include "shared.hpp"
#include "header_r.hpp"
#include "jelly.hpp"

#define LZZ_INLINE inline
namespace cnidaria
{
  struct register_data
  {
    baseInt & minH;
    string_t minKey;
    CNIDARIA_VAL_TYPE & key;
    j_mer_dna_t minMer;
    baseInt kmer_bytes;
    baseInt data_bytes;
    baseInt block_bytes;
  };
}
namespace cnidaria
{
  class cnidaria_header_rw : public cnidaria_header_r
  {
    baseInt lastHash;
  public:
    cnidaria_header_rw (string_t basenamel = DEFAULT_BASENAME);
    void save_header (header_data & hda, std::ofstream & outfile, string_t format);
    void save_header_complete_count (header_data & hda, std::ofstream & outfile);
    void save_summary (header_data & hda, string_t filename = "");
    void save_matrix (header_data & hda, string_t filename = "");
    void save_json_matrix (header_data & hda, string_t filename = "");
    void save_summary (header_data & hda, std::ofstream & outfile);
    void save_matrix (header_data & hda, std::ofstream & outfile);
    void save_json_matrix (header_data & hda, std::ofstream & outfile);
    void save_header_complete (header_data & hda, std::ofstream & outfile);
    void save_header_summary (header_data & hda, std::ofstream & outfile);
    void save_header_matrix (header_data & hda, std::ofstream & outfile);
    void save_header_json_matrix (header_data & hda, std::ofstream & outfile);
    void serialize_hash_table (header_data & hda, std::ofstream & outfile);
    void deserialize_hash_table (header_data & hda, std::ifstream & infile);
    void serialize_matrix (header_data & hda, std::ofstream & outfile);
    void serialize_complete_register (header_data & hda, std::ofstream & outfile, register_data const & d);
    void deserialize_complete_register (header_data & hda, std::ifstream & infile, register_data & d);
    void copy_complete_registers (header_data & hda, pos_type json_pos, std::ifstream & infile, std::ofstream & oufile, baseInt fileCount, baseInt numFiles);
  };
}
#undef LZZ_INLINE
#endif
