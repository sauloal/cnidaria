// header_r.cpp
//

#include "header_r.hpp"

#include <boost/filesystem.hpp>

#include "progressbar.hpp"

#define LZZ_INLINE inline
namespace cnidaria
{
  bool is_cnidaria (string_t filename)
                                              {
                string_t file_extension  = boost::filesystem::extension( filename );

                std::cout << "attempting load file " << filename << " whose extensions seems to be " << file_extension << std::endl;

                if        ( file_extension == cnidaria::EXT_COMPLETE  ) {
                        return true;

                } else if ( file_extension == cnidaria::EXT_SUMMARY   ) {
                        return true;

                } else if ( file_extension == cnidaria::EXT_MATRIX    ) {
                        return true;

                } else if ( file_extension == cnidaria::EXT_JMATRIX   ) {
                        return true;

                } else if ( file_extension == cnidaria::EXT_JELLYFISH ) {
                        return false;

                } else {
                        std::cout << "UNKNOWN EXTENSION: " << file_extension << std::endl;
                        exit(1);
                }
  }
}
namespace cnidaria
{
  string_t get_file_format (string_t filename)
                                                      {
                        string_t file_extension  = boost::filesystem::extension( filename );

                        std::cout << "attempting load file " << filename << " whose extensions seems to be " << file_extension << std::endl;

                        if        ( file_extension == EXT_COMPLETE  ) {
                                return FMT_COMPLETE;

                        } else if ( file_extension == EXT_SUMMARY   ) {
                                return FMT_SUMMARY;

                        } else if ( file_extension == EXT_MATRIX    ) {
                                return FMT_MATRIX;

                        } else if ( file_extension == EXT_JMATRIX   ) {
                                return FMT_JMATRIX;

                        } else if ( file_extension == EXT_JELLYFISH ) {
                                return FMT_JELLYFISH;

                        } else {
                                std::cout << "UNKNOWN EXTENSION: " << file_extension << std::endl;
                                exit(1);
                        }
  }
}
namespace cnidaria
{
  j_matrix_s::j_matrix_s ()
    : r (0), c (0)
                                         {}
}
namespace cnidaria
{
  j_matrix_s::j_matrix_s (baseInt R, baseInt C, baseint_vec_t COL)
    : r (R), c (C), columns (COL)
                                                                                              {}
}
namespace cnidaria
{
  header_data::header_data ()
    : infiles (NULL), srcfiles (NULL), matrix (NULL), hash_table (NULL), num_kmer_total_spp (NULL), num_kmer_valid_spp (NULL), complete_registers (0), num_infiles (0), num_srcfiles (0), num_combinations (0), min_val (0), max_val (0), save_every (0), num_pieces (0), piece_num (0), kmer_size (0), kmer_bytes (0), data_bytes (0), block_bytes (0), j_offset (0), j_size (0), j_matrices (NULL), version (0), filetype ("")
            {}
}
namespace cnidaria
{
  void header_data::print ()
                     {
            std::cout <<
            "number of files         " << infiles->size()            << "\n" <<
            "number of source files  " << srcfiles->size()           << "\n" <<
            "min_val                 " << min_val                    << "\n" <<
            "max_val                 " << max_val                    << "\n" <<
            "save_every              " << save_every                 << "\n" <<
            "num_pieces              " << num_pieces                 << "\n" <<
            "kmer_size               " << kmer_size                  << "\n" <<
            "kmer_bytes              " << kmer_bytes                 << "\n" <<
            "data_bytes              " << data_bytes                 << "\n" <<
            "block_bytes             " << block_bytes                << "\n" <<
            "version                 " << version                    << "\n" <<
            "filetype                " << filetype                   << "\n" <<
            "matrix size             " << matrix->size()             << "\n" <<
            "hash_table size         " << hash_table->size()         << "\n" <<
            "num_kmer_total_spp size " << num_kmer_total_spp->size() << "\n" <<
            "num_kmer_valid_spp size " << num_kmer_valid_spp->size() << "\n" <<
                        "j_offset                " << j_offset                   << "\n" <<
                        "j_size                  " << j_size                     << "\n" <<
                        "j_matrices              " << j_matrices->size()         << "\n" <<
            std::endl;

            std::cout <<
                        "file names              " << num_infiles << " " << infiles->size() << " ";
            for ( uint_t i = 0; i < num_infiles; ++i ) {
                std::cout << (*infiles)[i].c_str() << ", ";
            }
            std::cout << std::endl;

            std::cout <<
                        "source file names       " << num_srcfiles << " " << srcfiles->size() << " ";
            for ( uint_t i = 0; i < num_srcfiles; ++i ) {
                std::cout << (*srcfiles)[i].c_str() << ", ";
            }
            std::cout << std::endl;

            std::cout <<
                        "num_kmer_total_spp      " << num_infiles << " " << num_kmer_total_spp->size() << " ";
            for ( uint_t i = 0; i < num_infiles; ++i ) {
                std::cout << (*num_kmer_total_spp)[i] << ", ";
            }
            std::cout << std::endl;

            std::cout <<
                        "num_kmer_valid_spp      " << num_infiles << " " << num_kmer_valid_spp->size() << " ";
            for ( uint_t i = 0; i < num_infiles; ++i ) {
                std::cout << (*num_kmer_valid_spp)[i] << ", ";
            }
            std::cout << std::endl << std::endl;
  }
}
namespace cnidaria
{
  void header_data::add (header_data & hda)
                                       {



            min_val             = hda.min_val;
            max_val             = hda.max_val;
            save_every          = hda.save_every;
            num_pieces          = hda.num_pieces;
            piece_num           = hda.piece_num;
            kmer_size           = hda.kmer_size;
            kmer_bytes          = hda.kmer_bytes;
            data_bytes          = hda.data_bytes;
            block_bytes         = hda.block_bytes;
            version             = hda.version;
            filetype            = hda.filetype;
                        j_offset            = hda.j_offset;
                        j_size              = hda.j_size;

            num_infiles         = hda.infiles->size();
            num_srcfiles        = hda.srcfiles->size();
            complete_registers  = hda.complete_registers;
            num_combinations    = hda.num_combinations;
                        baseInt numMatrices = hda.j_matrices->size();

            (*srcfiles          ).clear();
            (*infiles           ).clear();
            (*num_kmer_total_spp).clear();
            (*num_kmer_valid_spp).clear();
                        (*j_matrices        ).clear();

            (*srcfiles          ).resize( num_srcfiles );
            (*infiles           ).resize( num_infiles  );
            (*num_kmer_total_spp).resize( num_infiles  );
            (*num_kmer_valid_spp).resize( num_infiles  );
            (*j_matrices        ).resize( numMatrices  );

            std::cout << " adding header :: in  files " << num_infiles  << " vs " << hda.infiles->size()  << std::endl;
            std::cout << " adding header :: src files " << num_srcfiles << " vs " << hda.srcfiles->size() << std::endl;


            for ( uint_t i = 0; i < num_infiles; ++i ) {
                (*infiles           )[i]  = (*hda.infiles           )[i];
                (*num_kmer_total_spp)[i] += (*hda.num_kmer_total_spp)[i];
                (*num_kmer_valid_spp)[i] += (*hda.num_kmer_valid_spp)[i];
                std::cout << " adding header :: in  file " << (*hda.infiles       )[i] << " total " << (*hda.num_kmer_total_spp)[i] << " valid " << (*hda.num_kmer_valid_spp)[i] << std::endl;
            }

            for ( uint_t i = 0; i < num_srcfiles; ++i ) {
                (*srcfiles          )[i]  = (*hda.srcfiles          )[i];
                std::cout << " adding header :: src file " << (*hda.srcfiles      )[i] << std::endl;
            }

                        for ( uint_t i = 0; i < numMatrices; ++i ) {
                (*j_matrices          )[i].r       = (*hda.j_matrices          )[i].r;
                                (*j_matrices          )[i].c       = (*hda.j_matrices          )[i].c;
                                (*j_matrices          )[i].columns = (*hda.j_matrices          )[i].columns;

                                std::cout << " adding header :: matrix " << i << " / " << numMatrices << " R: " << (*hda.j_matrices          )[i].r << " C: " << (*hda.j_matrices          )[i].c << "\n";
                                std::cout << " adding header :: matrix " << i << " / " << numMatrices << " V: ";

                                for ( uint_t j = 0; j < (*hda.j_matrices          )[i].columns.size(); ++j ) {
                                        if ( j > 0 ) {
                                                std::cout << ", ";
                                        }
                                        std::cout << (*hda.j_matrices          )[i].columns[j];
                                }

                                std::cout << std::endl;
            }

            baseInt matrixSize = matrix->size();
            std::cout << " adding header :: matrix " << matrixSize << " vs " << hda.matrix->size() << std::endl;
            if ( ( hda.matrix != NULL ) && ( hda.matrix->size() == num_infiles ) ) {
                std::cout << " adding header :: matrix " << matrixSize << " vs " << hda.matrix->size() << std::endl;

                (*matrix).clear();
                (*matrix).resize(num_infiles);

                for ( baseInt t = 0; t < num_infiles; ++t ) {
                    (*matrix)[t].clear();
                    (*matrix)[t].resize(num_infiles);
                    for ( baseInt u = 0; u < num_infiles; ++u ) {
                        (*matrix)[t][u].clear();
                        (*matrix)[t][u].resize(num_infiles);
                        for ( baseInt v = 0; v < num_infiles; ++v ) {
                            (*matrix)[t][u][v] += (*hda.matrix)[t][u][v];
                        }
                    }
                }

                std::cout << " adding header :: matrix finished" << std::endl;
            }


            if ( hda.hash_table != NULL ) {
                std::cout << " adding header :: hash table" << std::endl;
                for ( auto it01 = hda.hash_table->begin(); it01 != hda.hash_table->end(); ++it01 ) {
                    const auto&     key   = it01->first;
                    const uint64_t& val   = it01->second;
                    (*hash_table)[ key ] += val;
                }
                std::cout << " adding header :: hash table finished" << std::endl;
            }

            std::cout << " adding header :: finished" << std::endl;
  }
}
namespace cnidaria
{
  void header_data::merge (header_data & hda)
                                       {
            std::cout << " merging header" << std::endl;

            if ( infiles->size()  != hda.infiles->size()  ) { std::cout << "number of in  files differ " << infiles->size()  << " != " << hda.infiles->size()  << std::endl; exit(1); }
            if ( srcfiles->size() != hda.srcfiles->size() ) { std::cout << "number of src files differ " << srcfiles->size() << " != " << hda.srcfiles->size() << std::endl; exit(1); }
            if ( min_val          != hda.min_val          ) { std::cout << "min_val "     << min_val     << " differ" << std::endl; exit(1); }
            if ( max_val          != hda.max_val          ) { std::cout << "max_val "     << max_val     << " differ" << std::endl; exit(1); }
            if ( save_every       != hda.save_every       ) { std::cout << "save_every "  << save_every  << " differ" << std::endl; exit(1); }
            if ( num_pieces       != hda.num_pieces       ) { std::cout << "num_pieces "  << num_pieces  << " differ" << std::endl; exit(1); }
            if ( kmer_size        != hda.kmer_size        ) { std::cout << "kmer_size "   << kmer_size   << " differ" << std::endl; exit(1); }
            if ( kmer_bytes       != hda.kmer_bytes       ) { std::cout << "kmer_bytes "  << kmer_bytes  << " differ" << std::endl; exit(1); }
            if ( block_bytes      != hda.block_bytes      ) { std::cout << "block_bytes " << block_bytes << " differ" << std::endl; exit(1); }
            if ( version          != hda.version          ) { std::cout << "version "     << version     << " differ" << std::endl; exit(1); }
            if ( filetype         != hda.filetype         ) { std::cout << "filetype "    << filetype    << " differ" << std::endl; exit(1); }
            if ( j_size           != hda.j_size           ) { std::cout << "j_size "      << j_size      << " differ" << std::endl; exit(1); }


            std::cout << " merging header :: files " << infiles->size() << std::endl;

            for ( uint_t i = 0; i < num_infiles; ++i ) {
                if ( (*infiles)[i] != (*hda.infiles)[i] ) {
                    std::cout << "file differ " << (*infiles)[i] << " != " << (*hda.infiles)[i] << std::endl;
                    exit(1);
                }

                std::cout << " merging header :: file " << (*infiles)[i] << " total " << (*num_kmer_total_spp)[i] << " + " << (*hda.num_kmer_total_spp)[i] << " valid " << (*num_kmer_valid_spp)[i] << " + " << (*hda.num_kmer_valid_spp)[i] << std::endl;

                (*num_kmer_total_spp)[i] += (*hda.num_kmer_total_spp)[i];
                (*num_kmer_valid_spp)[i] += (*hda.num_kmer_valid_spp)[i];
            }


            for ( uint_t i = 0; i < num_srcfiles; ++i ) {
                if ( (*srcfiles)[i] != (*hda.srcfiles)[i] ) {
                    std::cout << "src file differ " << (*srcfiles)[i] << " != " << (*hda.srcfiles)[i] << std::endl;
                    exit(1);
                }



            }


            complete_registers += hda.complete_registers;
            num_combinations   += hda.num_combinations;

            if ( ( matrix != NULL ) && ( hda.matrix != NULL ) && ( matrix->size() == num_infiles ) && ( hda.matrix->size() == num_infiles ) ) {
                std::cout << " merging header :: matrix" << std::endl;

                for ( baseInt t = 0; t < num_infiles; ++t ) {
                    for ( baseInt u = 0; u < num_infiles; ++u ) {
                        for ( baseInt v = 0; v < num_infiles; ++v ) {
                                                        (*matrix)[t][u][v] += (*hda.matrix)[t][u][v];
                        }
                    }
                }
            } else {
                std::cout << " merging header :: NOT MERGING matrix" << std::endl;
                                std::cout << " merging header :: NOT MERGING matrix :: matrix is null: " << matrix << " hda.matrix is null " << hda.matrix << " matrix size " << matrix->size() << " != num infiles " << num_infiles << " hda.matrix size " << hda.matrix->size() << " != num infiles " << num_infiles << std::endl;

                        }

            if ( ( hash_table != NULL ) && ( hda.hash_table != NULL ) ) {
                for ( auto it01 = hda.hash_table->begin(); it01 != hda.hash_table->end(); ++it01 ) {
                    const auto&     key = it01->first;
                    const uint64_t& val = it01->second;
                    (*hash_table)[ key ] += val;
                }
            }
  }
}
namespace cnidaria
{
  cnidaria_header_r::cnidaria_header_r (string_t basenamel)
    : basename (basenamel), json_pos (0)
                                                                                                         {}
}
namespace cnidaria
{
  void cnidaria_header_r::openfile (std::ifstream & infile_, string_t filename)
                                                                                   {
                try {
                    infile_.open( filename, std::ios::in|std::ifstream::binary );
                } catch( std::ios_base::failure& e) {
                    std::cerr << "Failed to open header of file '" << filename << "' Error: " << e.what() << std::endl;
                    exit(1);
                }

                if (!infile_.good()) {
                    std::cerr   << "Failed to open header of file '" << filename << "'\n"
                                                                << "Failed to open header of file '" << filename << "' Error: " << std::strerror(errno) << "\n"
                                                                << "Failed to open header of file '" << filename << "' good : " << infile_.good()       << "\n"
                                                                << "Failed to open header of file '" << filename << "' eof  : " << infile_.eof()        << "\n"
                                                                << "Failed to open header of file '" << filename << "' fail : " << infile_.fail()       << "\n"
                                                                << "Failed to open header of file '" << filename << "' bad  : " << infile_.bad()        << std::endl;
                                        exit(1);
                }
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load (header_data & hda, string_t filename)
                                                                                                        {
                                std::ifstream infile_;

                                openfile( infile_, filename );

                load( hda, filename, infile_ );
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load (header_data & hda, string_t filename, std::ifstream & infile_)
                                                                                                                                {
                                if ( ! is_cnidaria( filename ) ) {
                                        std::cout << "file " << filename << " is not a cnidaria file" << std::endl;
                                        exit(1);
                                }





                                string_t file_extension = get_file_format( filename );

                                if        ( file_extension == FMT_COMPLETE ) {
                                        load_complete( hda, infile_ );

                                } else if ( file_extension == FMT_SUMMARY  ) {
                                        load_summary(  hda, infile_ );

                                } else if ( file_extension == FMT_MATRIX   ) {
                                        load_matrix(   hda, infile_ );

                                } else if ( file_extension == FMT_JMATRIX  ) {
                                        load_jmatrix(  hda, infile_ );

                                }
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load_complete (header_data & hda, string_t filename)
                                                                                               {
                std::ifstream infile_;

                                openfile( infile_, filename );

                std::cout << "parsing " << filename << std::endl;

                load_complete( hda, infile_ );
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load_complete (header_data & hda, std::ifstream & infile)
                                                                                               {
                infile.read( (char*)&json_pos, sizeof(baseInt) );

                std::cout << "loading complete. prev pos " << infile.tellg() << std::endl;
                std::cout << "loading complete. json pos " << json_pos << std::endl;
                std::cout << "loading complete. seeking"   << std::endl;

                infile.seekg(json_pos, infile.beg);

                std::cout << "loading complete. curr pos " << infile.tellg() << std::endl;

                read_header( hda, infile );

                if ( hda.filetype != FMT_COMPLETE ) {
                    std::cout << "not a complete file" << std::endl;
                    exit(1);
                }

                std::cout << "loading complete. late pos   " << infile.tellg() << std::endl;
                infile.seekg(sizeof(baseInt), infile.beg);
                std::cout << "loading complete. end  pos   " << infile.tellg() << std::endl;
                std::cout << "loading complete. end  state " << infile.good()  << " " << &infile << std::endl;
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load_matrix (header_data & hda, string_t filename)
                                                                                               {
                std::ifstream infile_;

                                openfile( infile_, filename );

                std::cout << "parsing " << filename << std::endl;

                load_matrix( hda, infile_ );
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load_matrix (header_data & hda, std::ifstream & infile)
                                                                                                           {
                read_header( hda, infile );

                if ( hda.filetype != FMT_MATRIX ) {
                    std::cout << "not a matrix file" << std::endl;
                    exit(1);
                }

                                deserialize_matrix( hda, infile );
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load_jmatrix (header_data & hda, string_t filename)
                                                                                               {
                std::ifstream infile_;

                                openfile( infile_, filename );

                std::cout << "parsing " << filename << std::endl;

                load_jmatrix( hda, infile_ );
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load_jmatrix (header_data & hda, std::ifstream & infile)
                                                                                               {
                std::cout << "loading json matrix. prev pos " << infile.tellg() << std::endl;

                string_t jsons = "";

                read_json( hda, infile, jsons );

                parse_header_json( hda, infile, jsons );

                if ( hda.filetype != FMT_JMATRIX ) {
                    std::cout << "not a json matrix file" << std::endl;
                    exit(1);
                }

                std::cout << "loading json matrix. end pos " << infile.tellg() << std::endl;
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load_summary (header_data & hda, string_t filename)
                                                                                                           {
                                std::ifstream infile_;

                                openfile( infile_, filename );

                std::cout << "parsing " << filename << std::endl;

                load_summary( hda, infile_ );
  }
}
namespace cnidaria
{
  void cnidaria_header_r::load_summary (header_data & hda, std::ifstream & infile)
                                                                                               {
                read_header( hda, infile );

                if ( hda.filetype != FMT_SUMMARY ) {
                    std::cout << "not a summary file" << std::endl;
                    exit(1);
                }

                                deserialize_matrix( hda, infile );
  }
}
namespace cnidaria
{
  void cnidaria_header_r::read_json (header_data & hda, std::ifstream & infile, string_t & jsons)
                                                                                                           {

























                                getline( infile, jsons);
  }
}
namespace cnidaria
{
  void cnidaria_header_r::read_header (header_data & hda, std::ifstream & infile)
                                                                                               {
                baseInt           json_size = 0;

                infile.read( (char*)&json_size, sizeof(baseInt) );

                std::cout << "size " << json_size << "\n";

                char jsonstr[ json_size ];

                infile.read( jsonstr, json_size );

                jsonstr[ json_size ] = '\0';

                std::cout << "json " << jsonstr << "\n";

                string_t jsons = jsonstr;

                parse_header_json( hda, infile, jsons  );
  }
}
namespace cnidaria
{
  void cnidaria_header_r::parse_header_json (header_data & hda, std::ifstream & infile, string_t & jsonstr)
                                                                                                             {
                                json_doc_t doc;
                doc.Parse( jsonstr.c_str() );

                std::cout << "parsed\n";

                if ( doc.HasParseError() ) {
                    std::cout << "parse error" << std::endl;
                    exit(1);
                }

                std::cout << "getting data\n";

                baseInt           num_infiles          = doc[ "num_infiles"        ].GetUint64();
                baseInt           num_srcfiles         = doc[ "num_srcfiles"       ].GetUint64();
                baseInt           num_combinations     = doc[ "num_combinations"   ].GetUint64();

                                baseInt           complete_registers   = doc[ "complete_registers" ].GetUint64();
                                baseInt           min_val              = doc[ "min_val"            ].GetUint64();
                                baseInt           max_val              = doc[ "max_val"            ].GetUint64();
                                baseInt           save_every           = doc[ "save_every"         ].GetUint64();
                                baseInt           num_pieces           = doc[ "num_pieces"         ].GetUint64();
                                baseInt           piece_num            = doc[ "piece_num"          ].GetUint64();
                baseInt           kmer_size            = doc[ "kmer_size"          ].GetUint64();
                baseInt           kmer_bytes           = doc[ "kmer_bytes"         ].GetUint64();
                baseInt           data_bytes           = doc[ "data_bytes"         ].GetUint64();
                baseInt           block_bytes          = doc[ "block_bytes"        ].GetUint64();
                                baseInt           j_offset             = doc[ "j_offset"           ].GetUint64();
                baseInt           j_size               = doc[ "j_size"             ].GetUint64();
                baseInt           j_matrices_size      = doc[ "j_matrices_size"    ].GetUint64();
                                uint_t            version              = doc[ "version"            ].GetUint();
                string_t          filetype             = doc[ "filetype"           ].GetString();

                hda.num_infiles        = num_infiles;
                hda.num_srcfiles       = num_srcfiles;
                hda.complete_registers = complete_registers;
                hda.min_val            = min_val;
                hda.max_val            = max_val;
                hda.save_every         = save_every;
                hda.num_pieces         = num_pieces;
                hda.piece_num          = piece_num;
                hda.kmer_size          = kmer_size;
                hda.kmer_bytes         = kmer_bytes;
                hda.data_bytes         = data_bytes;
                hda.block_bytes        = block_bytes;
                hda.num_combinations   = num_combinations;
                                hda.j_offset           = j_offset;
                                hda.j_size             = j_size;
                hda.version            = version;
                hda.filetype           = filetype;
                bool hasMatrix = doc.HasMember("matrix");

                std::cout << "checking version\n";
                if ( version != __CNIDARIA_VERSION__ ) {
                    std::cout << "version mismatch. fileversion: " << version << " cnidaria version: " << __CNIDARIA_VERSION__ << std::endl;
                    exit(1);
                }


                const json_val_t& d_infilenames        = doc[ "in_filenames"       ];
                const json_val_t& d_srcfilenames       = doc[ "src_filenames"      ];
                const json_val_t& d_num_kmer_valid_spp = doc[ "num_kmer_valid_spp" ];
                const json_val_t& d_num_kmer_total_spp = doc[ "num_kmer_total_spp" ];
                const json_val_t& d_j_matrices         = doc[ "j_matrices"         ];

                json_size_t       s_infilenames        = d_infilenames       .Size();
                json_size_t       s_srcfilenames       = d_srcfilenames      .Size();
                json_size_t       s_num_kmer_total_spp = d_num_kmer_total_spp.Size();
                json_size_t       s_num_kmer_valid_spp = d_num_kmer_valid_spp.Size();
                json_size_t       s_j_matrices         = d_j_matrices        .Size();

                if ( num_infiles  != s_infilenames ) {
                    std::cout << "number of in files in header differ: "  << s_infilenames        << " != " << num_infiles << std::endl;
                    exit( 1 );
                }

                if ( num_srcfiles != s_srcfilenames ) {
                    std::cout << "number of src files in header differ: " << s_srcfilenames       << " != " << num_srcfiles << std::endl;
                    exit( 1 );
                }

                if ( num_infiles  != s_num_kmer_total_spp ) {
                    std::cout << "number of files in header differ: "     << s_num_kmer_total_spp << " != " << num_infiles << std::endl;
                    exit( 1 );
                }

                if ( num_infiles  != s_num_kmer_valid_spp ) {
                    std::cout << "number of files in header differ: "     << s_num_kmer_valid_spp << " != " << num_infiles << std::endl;
                    exit( 1 );
                }

                                if ( s_j_matrices != j_matrices_size ) {
                                        std::cout << "number of matrices in header differ: "     << s_j_matrices << " != " << j_matrices_size << std::endl;
                    exit( 1 );
                                }

                std::cout << "resizing\n";
                                hda.infiles           ->resize( s_infilenames        );
                                hda.srcfiles          ->resize( s_srcfilenames       );
                                hda.num_kmer_total_spp->resize( s_num_kmer_total_spp );
                                hda.num_kmer_valid_spp->resize( s_num_kmer_valid_spp );
                                hda.j_matrices        ->resize( s_j_matrices         );

                std::cout << "loading src file names" << std::endl;
                for ( json_size_t k = 0; k < s_srcfilenames; ++k ) {
                    (*hda.srcfiles           )[k] = d_srcfilenames[k]     .GetString();
                }

                std::cout << "loading in file names" << std::endl;
                for ( json_size_t k = 0; k < s_infilenames; ++k ) {
                    (*hda.infiles           )[k] = d_infilenames[k]         .GetString();
                }

                std::cout << "loading kmer total" << std::endl;
                for ( json_size_t k = 0; k < s_num_kmer_total_spp; ++k ) {
                    (*hda.num_kmer_total_spp)[k] = d_num_kmer_total_spp[k].GetUint64();
                }

                std::cout << "loading kmer valid" << std::endl;
                for ( json_size_t k = 0; k < s_num_kmer_valid_spp; ++k ) {
                    (*hda.num_kmer_valid_spp)[k] = d_num_kmer_valid_spp[k].GetUint64();
                }

                std::cout << "loading jellyfish matrices" << std::endl;
                for ( json_size_t k = 0; k < s_j_matrices; ++k ) {
                                        const json_val_t& d_j_matrix         = d_j_matrices[k];
                                        uint64_t r = d_j_matrix["r"].GetUint64();
                                        uint64_t c = d_j_matrix["c"].GetUint64();
                                        uint64_t l = d_j_matrix["l"].GetUint64();

                                        const json_val_t& d_j_columns = d_j_matrix["columns"];
                                        uint64_t          s_j_columns = d_j_columns.Size();

                                        if ( s_j_columns != l ) {
                                                std::cout << " number of elements in matrix #" << k << " differ: " << s_j_columns << " vs " << l << std::endl;
                                                exit(1);
                                        }

                                        (*hda.j_matrices)[ k ].columns.resize( l );

                                        for ( json_size_t k1 = 0; k1 < l; ++k1 ) {
                                                uint64_t v = d_j_columns[ k1 ].GetUint64();
                                                (*hda.j_matrices)[ k ].columns[ k1 ] = v;
                                        }
                                        (*hda.j_matrices)[ k ].r = r;
                                        (*hda.j_matrices)[ k ].c = c;





























                }







                if ( hasMatrix ) {
                    const json_val_t& d_matrix             = doc[ "matrix"             ];

                    json_size_t       s_matrix             = d_matrix.Size();

                    if ( num_infiles != s_matrix ) {
                        std::cout << "number of files in header differ: " << s_matrix             << " != " << num_infiles << std::endl;
                        exit( 1 );
                    }

                    hda.matrix->resize( s_matrix );
                    for ( json_size_t t = 0; t < s_matrix; ++t ) {
                        (*hda.matrix)[t].resize( s_matrix );
                        const json_val_t& d_matrix_t = d_matrix[t];

                        for ( json_size_t u = 0; u < s_matrix; ++u ) {
                            (*hda.matrix)[t][u].resize( s_matrix );
                            const json_val_t& d_matrix_u = d_matrix_t[u];

                            for ( json_size_t v = 0; v < s_matrix; ++v ) {
                                baseInt val            = d_matrix_u[v].GetUint64();
                                (*hda.matrix)[t][u][v] = val;
                            }
                        }
                    }
                }
  }
}
namespace cnidaria
{
  void cnidaria_header_r::deserialize_matrix (header_data & hda, std::ifstream & infile)
                                                                                               {
                baseInt so          = sizeof( baseInt );
                baseInt len         = 0;
                baseInt num_infiles = hda.infiles->size();
                baseInt val         = 0;

                hda.matrix->resize( num_infiles );
                for ( baseInt t = 0; t < num_infiles; ++t ) {
                    (*hda.matrix)[t].resize( num_infiles );
                    for ( baseInt u = 0; u < num_infiles; ++u ) {
                        (*hda.matrix)[t][u].resize( num_infiles );
                    }
                }


                for ( baseInt t = 0; t < num_infiles; ++t ) {

                    for ( baseInt u = 0; u < num_infiles; ++u ) {

                        for ( baseInt v = 0; v < num_infiles; ++v ) {
                            if ( infile.good() ) {
                                infile.read(  reinterpret_cast<char *>(&val), so );
                                if ( infile.good() ) {
                                    (*hda.matrix)[t][u][v] = val;
                                    ++len;
                                } else {
                                    std::cout << "not enough registers :: EOF :: number registers: " << len << " x " << t  << " y " << u  << " z " << v << std::endl;
                                    exit(1);
                                }
                            } else {
                                std::cout << "not enough registers :: EOF :: number registers: " << len << " x " << t  << " y " << u  << " z " << v << std::endl;
                                exit(1);
                            }
                        }
                    }
                }

                baseInt endLen = num_infiles * num_infiles * num_infiles;
                if ( endLen != len ) {
                    std::cout << "not enough registers :: number registers: " << len << " necessary registers " <<  endLen << std::endl;
                    exit(1);
                }
  }
}
namespace cnidaria
{
  baseInt cnidaria_header_r::get_json_pos ()
                                    { return json_pos;
  }
}
#undef LZZ_INLINE
