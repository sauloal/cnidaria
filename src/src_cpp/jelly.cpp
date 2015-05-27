// jelly.cpp
//

#include "jelly.hpp"

#include <algorithm>
#include <cerrno>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <stdint.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <typeinfo>
#include <unistd.h>
#include <vector>
#include <boost/filesystem.hpp>

#define LZZ_INLINE inline
namespace jelly
{
  HeaderFileHolder::HeaderFileHolder ()
    : in (NULL), file_arg ("")
                                                                                        {}
}
namespace jelly
{
  HeaderFileHolder::HeaderFileHolder (string_t file_arg_l)
    : in (NULL), file_arg (file_arg_l)
                                                                                        { init();
  }
}
namespace jelly
{
  void HeaderFileHolder::init ()
                         {
                in         = new std::ifstream();

                try {
                    in->open(file_arg, std::ios::in|std::ios::binary);
                } catch( std::ios_base::failure& e) {
                    std::cerr << "Failed to open header of file '" << file_arg << "' Error: " << e.what() << std::endl;
                    exit(1);
                }


                if(!in->good()) {
                    std::cerr << "Failed to open header of file '" << file_arg << "' Error: " << std::strerror(errno) << "\n"
                              << "Failed to open header of file '" << file_arg << "' good : " << in->good()           << "\n"
                              << "Failed to open header of file '" << file_arg << "' eof  : " << in->eof()            << "\n"
                              << "Failed to open header of file '" << file_arg << "' fail : " << in->fail()           << "\n"
                              << "Failed to open header of file '" << file_arg << "' bad  : " << in->bad()            << "\n"
                              << "Failed to open header of file '" << file_arg << "'"                                 << std::endl;;
                    exit(1);




                }


                if(stat(file_arg.c_str(), &st) < 0) {
                    std::cerr << "Can't stat file '" << file_arg << "'" << std::endl;
                    exit(1);




                }
  }
}
namespace jelly
{
  jelly_iterator::jelly_iterator ()
    : HeaderFileHolder (""), last_id (0), last_file_coord (0), final_hash (0), last_hash (0), is_cnidaria (false), is_iteratable (false), is_valid (true), key (""), hash (0), prev_hash (0), val (CNIDARIA_VAL_TYPE()), tmp_val (0)
                                                                                                                                                                                                                                                                                      {}
}
namespace jelly
{
  jelly_iterator::jelly_iterator (string_t const & infile_name)
    : HeaderFileHolder (infile_name), last_id (0), last_file_coord (0), final_hash (0), last_hash (0), is_cnidaria (false), is_iteratable (false), is_valid (true), key (""), hash (0), prev_hash (0), val (CNIDARIA_VAL_TYPE()), tmp_val (0)
                                                                                                                                                                                                                                                                                      {




                hda                    =  header_data();

                hda.infiles            = &infiles;
                hda.srcfiles           = &srcfiles;
                hda.matrix             = &matrix;
                hda.hash_table         = &hash_table;
                hda.num_kmer_total_spp = &num_kmer_total_spp;
                hda.num_kmer_valid_spp = &num_kmer_valid_spp;
                hda.j_matrices         = &j_matrices_s;

                is_cnidaria            = cnidaria::is_cnidaria(     file_arg );
                string_t filetype      = cnidaria::get_file_format( file_arg );

                if ( ( filetype == cnidaria::FMT_SUMMARY ) || ( filetype == cnidaria::FMT_COMPLETE ) || ( filetype == cnidaria::FMT_JELLYFISH ) ) {
                    is_iteratable = true;
                }

                if ( is_cnidaria ) {
                    std::cout << " loading header of " << filetype << std::endl;

                    cnidaria_header hd = cnidaria_header();

                    std::cout << " sending infile " << in << " tell " << in->tellg() << std::endl;

                    hd.load( hda, file_arg, (*in) );

                    std::cout << " creating matrix " << in << " tell " << in->tellg() << std::endl;

                    gen_j_matrix();

                    std::cout << " matrix created" << std::endl;

                    baseInt  _length       =   st.st_size;
                    std::cout << " file size       " << _length << std::endl;



                    baseInt  tellg         =   in->tellg();
                    std::cout << " tellg           " << tellg   << std::endl;

                    baseInt  size          =   _length - tellg;
                    std::cout << " size            " << size    << std::endl;


                    if      ( filetype == cnidaria::FMT_SUMMARY ) {
                        last_file_coord    =   _length;
                        last_id            = ( size / get_block_bytes() ) - 1;
                    }
                    else if ( filetype == cnidaria::FMT_COMPLETE ) {
                        last_file_coord    =  hd.get_json_pos();
                        size               =  last_file_coord - in->tellg();
                        last_id            = ( size / get_block_bytes() ) - 1;
                    }

                } else {
                    jf_to_cnidaria();

                    baseInt  _length       =   st.st_size;
                    std::cout << " file size       " << _length << std::endl;
                    baseInt  tellg         =   in->tellg();
                    std::cout << " tellg           " << tellg   << std::endl;
                    baseInt  size          =   _length - get_j_offset();
                    std::cout << " size            " << size    << std::endl;
                    last_file_coord        =   _length;
                    std::cout << " last_file_coord " << last_file_coord << std::endl;
                    last_id                = ( size / get_block_bytes() ) - 1;
                    std::cout << " last_id         " << last_id         << std::endl;
                }





                Key::k( get_kmer_size() );






                val.resize( hda.num_infiles );

                if ( hda.data_bytes != val.num_blocks() ) {
                    std::cout << "hda.data_bytes (" << hda.data_bytes << ") != (" << val.num_blocks() << ")" << std::endl;
                    exit(1);
                }

                bytes1.clear();
                bytes1.resize( hda.data_bytes );

                is_valid = next(true);

                gen_last_hash();
                std::cout << " last_hash       " << last_hash       << std::endl;

                hda.print();
  }
}
namespace jelly
{
  string_t jelly_iterator::gen_key ()
                                                                               { return  mer.to_str();
  }
}
namespace jelly
{
  baseInt jelly_iterator::gen_hash ()
                                                                               { return  key_to_hash( mer );
  }
}
namespace jelly
{
  baseInt jelly_iterator::key_to_hash (Key const & key)
                                                                               { return  (*jmatrix).times( key ) & get_mask();
  }
}
namespace jelly
{
  CNIDARIA_VAL_TYPE jelly_iterator::get_val ()
                                                                               { return  val;
  }
}
namespace jelly
{
  CNIDARIA_VAL_TYPE * jelly_iterator::get_val_ptr ()
                                                                               { return &val;
  }
}
namespace jelly
{
  Key jelly_iterator::get_mer ()
                                                                               { return  mer;
  }
}
namespace jelly
{
  Key * jelly_iterator::get_mer_ptr ()
                                                                               { return &mer;
  }
}
namespace jelly
{
  string_t jelly_iterator::get_key ()
                                                                               { return  key;
  }
}
namespace jelly
{
  string_t * jelly_iterator::get_key_ptr ()
                                                                               { return &key;
  }
}
namespace jelly
{
  void jelly_iterator::get_mer (Key & m)
                                                                               { m =     mer;
  }
}
namespace jelly
{
  void jelly_iterator::get_key (string_t & k)
                                                                               { k =     key;
  }
}
namespace jelly
{
  void jelly_iterator::get_mer_ptr (Key * m)
                                                                               { m =    &mer;
  }
}
namespace jelly
{
  void jelly_iterator::get_key_ptr (string_t * k)
                                                                               { k =    &key;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_hash ()
                                                                               { return  hash;
  }
}
namespace jelly
{
  bool jelly_iterator::get_is_iteratable ()
                                                                               { return  is_iteratable;
  }
}
namespace jelly
{
  bool jelly_iterator::get_is_cnidaria ()
                                                                               { return  is_cnidaria;
  }
}
namespace jelly
{
  bool jelly_iterator::get_is_valid ()
                                                                               { return  is_valid;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_last_hash ()
                                                                               { return  last_hash;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_last_id ()
                                                                               { return  last_id;
  }
}
namespace jelly
{
  j_matrix_s_vec_t jelly_iterator::get_j_matrices ()
                                                                               { return *hda.j_matrices;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_j_size ()
                                                                               { return  hda.j_size;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_j_offset ()
                                                                               { return  hda.j_offset;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_kmer_size ()
                                                                               { return  hda.kmer_size;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_kmer_bits ()
                                                                               { return  hda.kmer_bytes * 8;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_kmer_bytes ()
                                                                               { return  hda.kmer_bytes;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_data_bytes ()
                                                                               { return  hda.data_bytes;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_block_bytes ()
                                                                               { return  hda.block_bytes;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_final_hash ()
                                                                               { return  hda.j_size - 1;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_mask ()
                                                                               { return  hda.j_size - 1;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_num_infiles ()
                                                                               { return  hda.num_infiles;
  }
}
namespace jelly
{
  baseInt jelly_iterator::get_num_srcfiles ()
                                                                               { return  hda.num_srcfiles;
  }
}
namespace jelly
{
  string_vec_t jelly_iterator::get_infiles ()
                                                                               { string_vec_t t = (*hda.infiles ); return t;
  }
}
namespace jelly
{
  string_vec_t jelly_iterator::get_srcfiles ()
                                                                               { string_vec_t t = (*hda.srcfiles); return t;
  }
}
namespace jelly
{
  void jelly_iterator::dump ()
                        {
                baseInt previous_hash = 0;
                baseInt current_hash  = 0;

                baseInt i = 0;
                while( next() ) {
                    current_hash = get_hash();
                    std::cout << (i+1) << "/" << get_last_id() << ": ";
                    print();
                    if ( current_hash < previous_hash ) {
                        std::cout << "ERROR IN HASH ORDER" << std::endl;
                        exit(1);
                    } else {
                        previous_hash = current_hash;
                    }
                    ++i;
                }
  }
}
namespace jelly
{
  void jelly_iterator::gen_last_hash ()
                                 {
                if ( ! is_valid      ) { return; }
                if ( ! is_iteratable ) { return; }
                bool ivo = is_valid;

                baseInt   record_len = get_block_bytes();

                baseInt   origCoord  = in->tellg();

                baseInt   maxCoord   = last_file_coord - record_len;

                          last_hash  = goto_coord( maxCoord );

                goto_coord( origCoord - record_len );


                is_valid = ivo;
  }
}
namespace jelly
{
  void jelly_iterator::print ()
                         {
                std::cout << get_mer() << " = " << get_hash() << " (" << in->tellg() << ")" << std::endl;
  }
}
namespace jelly
{
  void jelly_iterator::jf_to_cnidaria ()
                                  {



                j_file_header_t jf     =   j_file_header_t((*in));

                baseInt  offset        =   jf.offset();
                baseInt  counter_len   =   jf.counter_len();
                baseInt  key_len_bits  =   jf.key_len();
                baseInt  jSize         =   jf.size();

                baseInt  key_len_bytes = ( key_len_bits         / 8          ) + ( key_len_bits % 8 != 0 );
                baseInt  record_len    =   counter_len          + key_len_bytes;
                baseInt  kmer_size     =   key_len_bits         / 2;

                jmatrix.reset( new j_rbm_matrix_t( jf.matrix() ) );
                baseInt       r        =  (*jmatrix).r();
                baseInt       c        =  (*jmatrix).c();
                baseint_vec_t m;

                for(unsigned int i = 0; i < c; ++i) {
                    m.push_back( (*jmatrix)[i] );
                }

                hda.j_matrices->push_back( j_matrix_s( r, c, m ) );
                hda.infiles   ->push_back( file_arg              );
                hda.srcfiles  ->push_back( file_arg              );
                hda.num_infiles  = 1;
                hda.num_srcfiles = 1;
                hda.kmer_size    = kmer_size;
                hda.kmer_bytes   = key_len_bytes;
                hda.data_bytes   = counter_len;
                hda.block_bytes  = record_len;
                hda.j_offset     = offset;
                hda.j_size       = jSize;
                hda.filetype     = cnidaria::FMT_JELLYFISH;

                hda.num_kmer_total_spp->push_back(0);
                hda.num_kmer_valid_spp->push_back(0);
  }
}
namespace jelly
{
  void jelly_iterator::gen_j_matrix ()
                                {
                std::cout << "regenerating binary matrix with " << (*hda.j_matrices).size() << " matrices" << std::endl;

                if ( (*hda.j_matrices).size() != 1 ) {
                    std::cout << "wrong number of matrices" << std::endl;
                    exit(1);
                }

                j_matrix_s matrix1 = (*hda.j_matrices)[0];










                jmatrix.reset( new j_rbm_matrix_t( matrix1.columns.data(), matrix1.r, matrix1.c ) );

                std::cout << "regenerated  binary matrix from R: " << jmatrix->r() << " C: " << jmatrix->c() << std::endl;
  }
}
namespace jelly
{
  bool jelly_iterator::next (bool binaring)
                                                                      {
                if ( ! is_valid                       ) { return false; }
                if ( ! is_iteratable                  ) { return false; }
                if ( ! in->good()                     ) { return false; }
                if (   in->tellg() >= last_file_coord ) { return false; }



                mer.template read<1>((*in));
                val.reset();






                if ( is_cnidaria ) {
                    in->read( reinterpret_cast<char *>(&bytes1[0]), hda.data_bytes );
                    boost::from_block_range( bytes1.begin(), bytes1.end(), val );

                } else {
                    tmp_val = 0;
                    in->read((char*)&tmp_val, hda.data_bytes);
                    val[0] = true;

                }

                key    = gen_key();

                hash   = gen_hash();








                if ( ! binaring ) {
                    if ( prev_hash == 0 ) {
                        prev_hash = hash;

                    } else {
                        if ( prev_hash > hash ) {
                            std::cout << file_arg << " :: previous hash " << prev_hash << " GRATER THAN current hash " << hash << std::endl;







                            exit(1);

                        } else {
                            prev_hash = hash;

                        }
                    }

                    if ( hash > 0 && last_hash > 0 && hash >= last_hash ) { return false; }

                }

                return in->good();
  }
}
namespace jelly
{
  baseInt jelly_iterator::goto_coord (baseInt coord)
                                                                              {
                if ( ! is_iteratable ) { return 0; }


                in->seekg(coord, in->beg);


                is_valid = next(true);


                return get_hash();
  }
}
namespace jelly
{
  void jelly_iterator::seekHash (baseInt req_hash)
                                                                              {
                if ( ! is_valid      ) { return; }
                if ( ! is_iteratable ) { return; }

                if ( ( req_hash > 0 ) && ( get_hash() < req_hash ) ) {
                    baseInt record_len = get_block_bytes();

                    std::cout << "BINARYING" << std::endl;

                    baseInt   origCoord  = in->tellg();




                    baseInt   maxCoord   = last_file_coord - record_len;

                    baseInt   leftId     = 0;
                    baseInt   rightId    = last_id;
                    baseInt   midId      = rightId / 2;
                    baseInt   endId      = 0;

                    baseInt   leftCoord  = origCoord + ( leftId  * record_len );
                    baseInt   midCoord   = origCoord + ( midId   * record_len );

                    baseInt   rightCoord = maxCoord;
                    baseInt   endCoord   = 0;

                    baseInt   leftPos    = goto_coord( leftCoord  );
                    baseInt   midPos     = goto_coord( midCoord   );
                    baseInt   rightPos   = goto_coord( rightCoord );
                    baseInt   endPos     = 0;

                    std::fprintf( stdout, "INITIAL origCoord %'15llu minPos     %'15llu maxCoord %'15llu record_len %'15llu last_id %'15llu last_coord %'15llu\n", origCoord, req_hash, maxCoord, record_len, last_id, rightCoord );
                    std::fprintf( stdout, "INITIAL leftId    %'15llu leftCoord  %'15llu leftPos  %'15llu\n", leftId , leftCoord , leftPos  );
                    std::fprintf( stdout, "INITIAL midId     %'15llu midCoord   %'15llu midPos   %'15llu\n", midId  , midCoord  , midPos   );
                    std::fprintf( stdout, "INITIAL rightId   %'15llu rightCoord %'15llu rightPos %'15llu\n", rightId, rightCoord, rightPos );

                    std::cout << std::endl;

                    if ( req_hash > rightPos ) {
                        std::fprintf( stdout, "REQUIRED HASH %'15llu GREATER THAN MAXIMUM HASH %'15llu\n\n", req_hash, rightPos );
                        endCoord = rightCoord + (2*record_len);
                        endPos   = rightPos   + 1;
                        endId    = rightId    + 1;
                        is_valid = false;

                    } else {
                        while ( true ) {
                            if      (( leftPos == midPos   ) || ( leftPos == rightPos   ) || ( rightPos == midPos    ) ){
                                if      ( leftPos >= req_hash ) {

                                  endId    = leftId;
                                  endCoord = leftCoord;
                                  endPos   = leftPos;
                                }
                                else if ( rightPos >= req_hash ){

                                  endId    = rightId;
                                  endCoord = rightCoord;
                                  endPos   = rightPos;
                                }
                                break;

                            }
                            else if ( req_hash == leftPos  ) {
                                endId    = leftId;
                                endCoord = leftCoord;
                                endPos   = leftPos;

                                break;

                            }
                            else if ( req_hash == midPos   ) {
                                endId    = midId;
                                endCoord = midCoord;
                                endPos   = midPos;

                                break;

                            }
                            else if ( req_hash == rightPos ) {
                                endId    = rightId;
                                endCoord = rightCoord;
                                endPos   = rightPos;

                                break;

                            }
                            else if ( req_hash <  midPos   ) {
                                rightId    = midId;
                                rightCoord = midCoord;
                                rightPos   = midPos;

                                midId      = leftId    + ((rightId - leftId) / 2);
                                midCoord   = origCoord + ( midId   * record_len  );
                                midPos     = goto_coord( midCoord   );

                            } else {
                                leftId     = midId;
                                leftCoord  = midCoord;
                                leftPos    = midPos;

                                midId      = leftId    + ((rightId - leftId) / 2);
                                midCoord   = origCoord + ( midId   * record_len  );
                                midPos     = goto_coord( midCoord   );

                            }
                        }
                    }

                    goto_coord( endCoord );



                    std::cout << " sizeof baseInt  " << sizeof(baseInt )               << std::endl;
                    std::cout << " sizeof llu      " << sizeof(long long unsigned int) << std::endl;

                    baseInt  currCoord = (baseInt)in->tellg()     - record_len;
                    baseInt  currId    = ((currCoord - origCoord) / record_len);

                    std::fprintf( stdout, "FOUND minPos %'15llu\n", req_hash );
                    std::fprintf( stdout, "FINAL   leftId  %'40llu leftCoord  %'15llu leftPos  %'15llu\n", leftId , leftCoord , leftPos           );
                    std::fprintf( stdout, "FINAL   midId   %'40llu midCoord   %'15llu midPos   %'15llu\n", midId  , midCoord  , midPos            );
                    std::fprintf( stdout, "FINAL   rightId %'40llu rightCoord %'15llu rightPos %'15llu\n", rightId, rightCoord, rightPos          );
                    std::fprintf( stdout, "FINAL   endId   %'40llu endCoord   %'15llu endPos   %'15llu\n", endId  , endCoord  , endPos            );
                    std::fprintf( stdout, "FINAL   currId  %'40llu currCoord  %'15llu currPos  %'15llu\n", currId , currCoord , get_hash()        );
                    std::fprintf( stdout, "FINAL   key     %-31s\n"                                                           , get_key().c_str() );

                    std::cout << std::endl;
                }
  }
}
#undef LZZ_INLINE
