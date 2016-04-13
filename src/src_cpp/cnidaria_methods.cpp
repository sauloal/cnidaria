// cnidaria_methods.cpp
//

#include "cnidaria_methods.hpp"
#define LZZ_INLINE inline
namespace cnidaria
{
  baseInt get_max_threads ()
                              {
        return std::thread::hardware_concurrency();
  }
}
namespace cnidaria
{
  cnidaria_db::cnidaria_db ()
                              {}
}
namespace cnidaria
{
  cnidaria_db::cnidaria_db (string_vec_t & srcfilesl, string_t basenamel)
    : srcfiles (srcfilesl), basename (basenamel), min_val_d (DEFAULT_MIN_NUMBER_SPP_PERC), max_val_d (DEFAULT_MAX_NUMBER_SPP_PERC), min_val_i (0), max_val_i (0), export_complete (false), export_summary (false), export_matrix (true), complete_registers (0), num_infiles (0), num_srcfiles (srcfiles.size()), ext_outfile_ (NULL), j_offset (0), j_size (0)
                {

                jfheap        jfh( (*this), 1, 0, "db stats" );
                infiles     = jfh.get_infiles();
                num_infiles = infiles.size();
                j_matrices  = jfh.get_j_matrices();
                j_offset    = jfh.get_j_offset();
                j_size      = jfh.get_j_size();
                max_val_i   = num_infiles;
                hd          = cnidaria_header_rw ();

                num_kmer_total_spp.resize( num_infiles );
                num_kmer_valid_spp.resize( num_infiles );

                set_min_val( min_val_d );
                set_max_val( max_val_d );

                matrix.resize( num_infiles );
                for ( baseInt t = 0; t < num_infiles; ++t ) {
                    matrix[t].resize( num_infiles );
                    for ( baseInt u = 0; u < num_infiles; ++u ) {
                        matrix[t][u].resize( num_infiles );
                        for ( baseInt v = 0; v < num_infiles; ++v ) {
                            matrix[t][u][v] = 0;
                        }
                    }
                }
  }
}
namespace cnidaria
{
  void cnidaria_db::set_min_val (double mi)
                                               { min_val_d   = mi; baseInt min_val = (baseInt)(num_infiles * mi); set_min_val(min_val);
  }
}
namespace cnidaria
{
  void cnidaria_db::set_max_val (double ma)
                                               { max_val_d   = ma; baseInt max_val = (baseInt)(num_infiles * ma); set_max_val(max_val);
  }
}
namespace cnidaria
{
  void cnidaria_db::set_min_val (baseInt mi)
                                               {
                std::cout << "set min val " << mi;
                min_val_i   = mi;
                if ( min_val_i > max_val_i ) { min_val_i = max_val_i; }
                std::cout << " set to " << min_val_i << " max val " << max_val_i << "\n";
  }
}
namespace cnidaria
{
  void cnidaria_db::set_max_val (baseInt ma)
                                               {
                std::cout << "set max val " << ma;
                max_val_i   = ma;
                if ( max_val_i < min_val_i   ) { max_val_i = min_val_i;   }
                if ( max_val_i > num_infiles ) { max_val_i = num_infiles; }
                std::cout << " set to " << max_val_i << " min val " << min_val_i << "\n";
  }
}
namespace cnidaria
{
  void cnidaria_db::set_complete_registers (baseInt cr)
                                                                        { complete_registers = cr;
  }
}
namespace cnidaria
{
  baseInt cnidaria_db::get_complete_registers ()
                                                                                    { return complete_registers;
  }
}
namespace cnidaria
{
  void cnidaria_db::set_export_summary (bool s)
                                               { export_summary  = s;
  }
}
namespace cnidaria
{
  void cnidaria_db::set_export_matrix (bool s)
                                               { export_matrix   = s;
  }
}
namespace cnidaria
{
  void cnidaria_db::set_export_complete (header_data & hda, bool s, string_t filename)
                                                                                       { if ( filename=="" ) { filename=basename; }; if ( s ) { enable_complete( hda, filename ); } else { disable_complete(); };
  }
}
namespace cnidaria
{
  void cnidaria_db::enable_summary ()
                                               { export_summary  = true;
  }
}
namespace cnidaria
{
  void cnidaria_db::disable_summary ()
                                               { export_summary  = false;
  }
}
namespace cnidaria
{
  void cnidaria_db::enable_matrix ()
                                               { export_matrix   = true;
  }
}
namespace cnidaria
{
  void cnidaria_db::disable_matrix ()
                                               { export_matrix   = false;
  }
}
namespace cnidaria
{
  void cnidaria_db::disable_complete ()
                                               { export_complete = false;
  }
}
namespace cnidaria
{
  void cnidaria_db::enable_complete (header_data & hda, string_t filename)
                                                                                       {
                if ( filename=="" ) { filename=basename; };
                if ( ! export_complete ) {
                    if ( ext_outfile_ == NULL ) {
                        ext_outfile_ = new std::ofstream();
                        ext_outfile_->open( filename + EXT_COMPLETE, std::ifstream::binary );






                        if (!ext_outfile_->good()) {
                            std::cout << "error opening " << filename << EXT_COMPLETE << std::endl;
                            exit(1);
                        }
                    } else {
                        std::cout << "asked to open complete file with open file handle" << std::endl;
                        exit(1);
                    }

                    amendHeaderData( hda );
                    hd.save_header_complete( hda, (*ext_outfile_) );
                    export_complete = true;
                }
  }
}
namespace cnidaria
{
  void cnidaria_db::close_complete (header_data & hda)
                                                                 {
                if ( export_complete ) {
                    if ( ext_outfile_ != NULL ) {
                        if ( ! ext_outfile_->good() ) {
                            std::cout << "\n"
                                      << "error saving header complete count Error  : " << std::strerror(errno)    << "\n"
                                      << "error saving header complete count good   : " << ext_outfile_->good()    << "\n"
                                      << "error saving header complete count fail   : " << ext_outfile_->fail()    << "\n"
                                      << "error saving header complete count bad    : " << ext_outfile_->bad()     << "\n"
                                      << "error saving header complete count rdstate: " << ext_outfile_->rdstate() << "\n"
                                      << "error saving header complete count eof    : " << ext_outfile_->eof()     << std::endl;
                            exit(1);
                        }

                        std::cout << "closing complete" << std::endl;

                        amendHeaderData( hda );

                        hd.save_header_complete_count( hda, (*ext_outfile_) );

                        std::cout << "complete file closed" << std::endl;

                        ext_outfile_->close();

                        export_complete = false;
                    } else {
                        std::cout << "asked to close complete file with closed file handle" << std::endl;
                        exit(1);
                    }
                } else {
                    std::cout << "asked to close complete file when it was not enabled" << std::endl;

                }
  }
}
namespace cnidaria
{
  void cnidaria_db::amendHeaderData (header_data & hda)
                                                                 {
                hda.infiles            = &infiles;
                hda.srcfiles           = &srcfiles;
                hda.matrix             = &matrix;
                hda.hash_table         = &hash_table;
                hda.num_kmer_total_spp = &num_kmer_total_spp;
                hda.num_kmer_valid_spp = &num_kmer_valid_spp;

                hda.min_val            =  min_val_i;
                hda.max_val            =  max_val_i;
                hda.complete_registers =  complete_registers;
                hda.num_infiles        =  num_infiles;
                hda.num_srcfiles       =  num_srcfiles;
                hda.num_combinations   =  hash_table.size();

                hda.j_offset           =  j_offset;
                hda.j_size             =  j_size;
                hda.j_matrices         = &j_matrices;
  }
}
namespace cnidaria
{
  void cnidaria_db::save_all (header_data & hda, string_t filename)
                                                                                       {
                if ( filename=="" ) { filename=basename; };
                save_summary(     hda, filename );
                save_matrix(      hda, filename );
                save_json_matrix( hda, filename );
                close_complete(   hda           );
  }
}
namespace cnidaria
{
  void cnidaria_db::load_all (header_data & hda, string_t filename)
                                                                                       {
                if ( filename=="" ) { filename=basename; };
                load_summary( hda, filename );
                load_matrix(  hda, filename );
  }
}
namespace cnidaria
{
  void cnidaria_db::load (header_data & hda, string_t filename)
                                                                                       {
                if ( filename=="" ) { filename=basename; };
                amendHeaderData( hda );
                hd.load( hda, filename );
  }
}
namespace cnidaria
{
  void cnidaria_db::save_summary (header_data & hda, string_t filename)
                                                                                       {
                if ( filename=="" ) { filename=basename; };
                if ( export_summary ) {
                    std::cout << "saving summary to " << filename << std::endl;
                    amendHeaderData( hda );
                    hd.save_summary( hda, filename );
                }
  }
}
namespace cnidaria
{
  void cnidaria_db::load_summary (header_data & hda, string_t filename)
                                                                                       {
                if ( filename=="" ) { filename=basename; };
                amendHeaderData( hda );
                hd.load_summary( hda, filename );
  }
}
namespace cnidaria
{
  void cnidaria_db::save_matrix (header_data & hda, string_t filename)
                                                                                       {
                if ( filename=="" ) { filename=basename; };
                if ( export_matrix ) {
                    std::cout << "saving matrix to " << filename << std::endl;
                    amendHeaderData( hda );
                    hd.save_matrix(  hda, filename );
                }
  }
}
namespace cnidaria
{
  void cnidaria_db::save_json_matrix (header_data & hda, string_t filename)
                                                                                       {
                if ( filename=="" ) { filename=basename; };
                amendHeaderData(     hda );
                hd.save_json_matrix( hda, filename );
  }
}
namespace cnidaria
{
  void cnidaria_db::load_matrix (header_data & hda, string_t filename)
                                                                                       {}
}
namespace cnidaria
{
  void cnidaria_db::serialize_complete_register (header_data & hda, register_data d)
                                                                                  {
                if ( export_complete ) {
                    hd.serialize_complete_register( hda, (*ext_outfile_), d );

                    ++complete_registers;

                }
  }
}
namespace cnidaria
{
  void cnidaria_db::merge (cnidaria_db & data)
                                                                      {

                for ( baseInt n = 0; n < num_kmer_total_spp.size(); ++n ) {





                    num_kmer_total_spp[ n ] += data.num_kmer_total_spp[ n ];
                }


                for ( baseInt n = 0; n < num_kmer_valid_spp.size(); ++n ) {
                    num_kmer_valid_spp[ n ] += data.num_kmer_valid_spp[ n ];
                }



                for ( baseInt t = 0; t < num_infiles; ++t ) {

                    for ( baseInt u = 0; u < num_infiles; ++u ) {

                        for ( baseInt v = 0; v < num_infiles; ++v ) {
                            matrix[t][u][v] += data.matrix[t][u][v];
                        }
                    }
                }


                for ( auto&k: data.hash_table ) {
                    hash_table[ k.first ] += k.second;
                }
  }
}
namespace cnidaria
{
  void cnidaria_db::add (CNIDARIA_VAL_TYPE & resb, baseInt & numValid)
                                                                                           {
                if ( export_summary || export_matrix ) {
                    if ( (numValid >= min_val_i) && (numValid <= max_val_i) ) {
                        if ( export_summary ) {
                            ++hash_table[ resb ];
                        }

                        if ( export_matrix ) {







                            for ( baseInt t = 0; t < num_infiles; ++t ) {

                                if ( resb[t] ) {
                                                                        ++num_kmer_valid_spp[t];


                                    for ( baseInt u = t+1; u < num_infiles; ++u ) {
                                        if ( resb[u] ) {



                                            ++matrix[ t ][ u ][ numValid-1 ];
                                            ++matrix[ u ][ t ][ numValid-1 ];

                                        }
                                    }
                                }
                            }
                        }
                    }
                }
  }
}
namespace cnidaria
{
  heapdata::heapdata ()
    : name (""), valid (false), kmers (0), it (NULL)
                                                                                      {}
}
namespace cnidaria
{
  heapdata::heapdata (string_t const & n)
    : name (n), valid (true), kmers (0), it (NULL)
                                                                                      {
                it         = new j_file_iterator_t( name );

                print();
  }
}
namespace cnidaria
{
  void heapdata::print ()
                                               {
                std::cout << "heap data :: print :: "                <<
                            " name "           << get_name()         <<
                            " valid "          << get_valid()        <<
                            " kmers "          << get_kmers()        <<
                            " kmer size: "     << get_kmer_size()    <<
                            " kmer bytes: "    << get_kmer_bytes()   <<
                            " data bytes: "    << get_data_bytes()   <<
                            " block bytes: "   << get_block_bytes()  <<
                            " final hash: "    << get_final_hash()   <<
                            " hash: "          << get_hash()         <<
                            " num src files: " << get_num_srcfiles() <<
                            " key: "           << get_key()          <<
                            " mer: "           << get_mer()          <<
                            " val: "           << get_val()          <<
                            std::endl;
  }
}
namespace cnidaria
{
  bool heapdata::next ()
                                              {
                bool   r  = it->next();

                if ( r ) {
                    ++kmers;
                }

                return r;
  }
}
namespace cnidaria
{
  void heapdata::seekHash (uint64_t req_hash)
                                                                     {
                it->seekHash( req_hash );
  }
}
namespace cnidaria
{
  string_t const heapdata::get_name ()
                                                          { return name;
  }
}
namespace cnidaria
{
  bool const heapdata::get_valid ()
                                                          { return valid;
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_kmers ()
                                                          { return kmers;
  }
}
namespace cnidaria
{
  string_t const heapdata::get_key ()
                                                          { return it->get_key();
  }
}
namespace cnidaria
{
  string_t * heapdata::get_key_ptr ()
                                                          { return it->get_key_ptr();
  }
}
namespace cnidaria
{
  j_mer_dna_t const heapdata::get_mer ()
                                                          { return it->get_mer();
  }
}
namespace cnidaria
{
  j_mer_dna_t * heapdata::get_mer_ptr ()
                                                          { return it->get_mer_ptr();
  }
}
namespace cnidaria
{
  CNIDARIA_VAL_TYPE const heapdata::get_val ()
                                                          { return it->get_val();
  }
}
namespace cnidaria
{
  CNIDARIA_VAL_TYPE * heapdata::get_val_ptr ()
                                                          { return it->get_val_ptr();
  }
}
namespace cnidaria
{
  j_matrix_s_vec_t const heapdata::get_j_matrices ()
                                                          { return it->get_j_matrices();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_j_size ()
                                                          { return it->get_j_size();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_j_offset ()
                                                          { return it->get_j_offset();
  }
}
namespace cnidaria
{
  string_vec_t const heapdata::get_infiles ()
                                                          { return it->get_infiles();
  }
}
namespace cnidaria
{
  string_vec_t const heapdata::get_srcfiles ()
                                                          { return it->get_srcfiles();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_kmer_size ()
                                                          { return it->get_kmer_size();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_kmer_bytes ()
                                                          { return it->get_kmer_bytes();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_data_bytes ()
                                                          { return it->get_data_bytes();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_block_bytes ()
                                                          { return it->get_block_bytes();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_final_hash ()
                                                          { return it->get_final_hash();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_hash ()
                                                          { return it->get_hash();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_last_hash ()
                                                          { return it->get_last_hash();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_num_srcfiles ()
                                                          { return it->get_num_srcfiles();
  }
}
namespace cnidaria
{
  baseInt const heapdata::get_num_infiles ()
                                                          { return it->get_num_infiles();
  }
}
namespace cnidaria
{
  void heapdata::set_valid (bool v)
                                                          { valid = v;
  }
}
namespace cnidaria
{
  jfheap::jfheap ()
    : minH (0), lminH (0), numValid (0), num_infiles (0), num_srcfiles (0), minValid (0), num_pieces (0), piece_num (0), piecehash (0), beginhash (0), endhash (0), finalhash (0), lasthash (0), tmp_offset (0), tmp_num_infiles (0), name (""), resb (CNIDARIA_VAL_TYPE()), rest (CNIDARIA_VAL_TYPE())
                                                                                                                                                                                                                                                                                                                                                                                                                    {}
}
namespace cnidaria
{
  jfheap::jfheap (cnidaria_db & hash_tableL)
    : minH (0), lminH (0), numValid (0), num_infiles (0), num_srcfiles (0), minValid (0), num_pieces (0), piece_num (0), piecehash (0), beginhash (0), endhash (0), finalhash (0), lasthash (0), tmp_offset (0), tmp_num_infiles (0), name (""), resb (CNIDARIA_VAL_TYPE()), rest (CNIDARIA_VAL_TYPE()), hash_table (&hash_tableL)
                                                                                                                                                                                                                                                                                                                                                                                                                                              {
                init();
  }
}
namespace cnidaria
{
  jfheap::jfheap (cnidaria_db & hash_tableL, baseInt num_piecesl, baseInt piece_numl, string_t namel)
    : minH (0), lminH (0), numValid (0), num_infiles (0), num_srcfiles (0), minValid (0), num_pieces (num_piecesl), piece_num (piece_numl), piecehash (0), beginhash (0), endhash (0), finalhash (0), lasthash (0), tmp_offset (0), tmp_num_infiles (0), name (namel), resb (CNIDARIA_VAL_TYPE()), rest (CNIDARIA_VAL_TYPE()), hash_table (&hash_tableL)
                                                                                                                                                                                                                                                                                                                                                                                                                                              {
                init();

                std::cout   << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | kmer_size         : " << get_kmer_size()       << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | kmer_bytes        : " << get_kmer_bytes()      << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | data_bytes in     : " << get_data_bytes_in()   << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | data_bytes out    : " << get_data_bytes_out()  << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | block_bytes in    : " << get_block_bytes_in()  << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | block_bytes out   : " << get_block_bytes_out() << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | num pieces        : " << num_pieces            << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | piece num         : " << piece_num             << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | final hash        : " << finalhash             << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | last hash         : " << lasthash              << "\n";

                piecehash   = get_final_hash() / num_pieces;
                beginhash   = piecehash        * piece_num;
                endhash     = beginhash        + piecehash;

                std::cout   << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | piece hash        : " << piecehash             << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | end   hash        : " << endhash               << "\n"
                            << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | seeking begin hash: " << beginhash             << std::endl;

                seekHash( beginhash );

                std::cout   << " heap piece " << ( piece_num + 1 ) << " / " << num_pieces << " | '" << name << "' | sought begin hash : " << beginhash << std::endl;
  }
}
namespace cnidaria
{
  j_matrix_s_vec_t jfheap::get_j_matrices ()
                                                              { return data[ 0 ]->get_j_matrices();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_begin_hash ()
                                                                          { return beginhash;
  }
}
namespace cnidaria
{
  baseInt jfheap::get_end_hash ()
                                                                          { return endhash;
  }
}
namespace cnidaria
{
  baseInt jfheap::get_last_hash ()
                                                                          { return lasthash;
  }
}
namespace cnidaria
{
  baseInt jfheap::get_j_size ()
                                                              { return data[ 0 ]->get_j_size();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_j_offset ()
                                                              { return data[ 0 ]->get_j_offset();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_kmer_size ()
                                                              { return data[ 0 ]->get_kmer_size();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_kmer_bytes ()
                                                              { return data[ 0 ]->get_kmer_bytes();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_final_hash ()
                                                              { return data[ 0 ]->get_final_hash();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_block_bytes_in ()
                                                              { return data[ 0 ]->get_block_bytes();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_data_bytes_in ()
                                                              { return data[ 0 ]->get_data_bytes();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_block_bytes_out ()
                                                              { return get_data_bytes_out() + get_kmer_bytes();
  }
}
namespace cnidaria
{
  baseInt jfheap::get_data_bytes_out ()
                                                              {
                CNIDARIA_VAL_TYPE b1      = CNIDARIA_VAL_TYPE( num_infiles );
                                return b1.num_blocks();
  }
}
namespace cnidaria
{
  string_vec_t jfheap::get_srcfiles ()
                                                            {
                string_vec_t af;
                for ( baseInt f = 0; f < data.size(); ++f ) {
                    af.push_back( data[f]->get_name() );
                }
                return af;
  }
}
namespace cnidaria
{
  string_vec_t jfheap::get_infiles ()
                                                            {
                string_vec_t af;
                for ( baseInt f = 0; f < data.size(); ++f ) {
                    string_vec_t fs = data[f]->get_infiles();
                    for ( baseInt g = 0; g < fs.size(); ++g ) {
                        af.push_back( fs[g] );
                    }
                }
                return af;
  }
}
namespace cnidaria
{
  void jfheap::setMinValid (baseInt minValidl)
                                                  { minValid = minValidl;
  }
}
namespace cnidaria
{
  void jfheap::init ()
                        {
                std::cout << " INITIALIZING HEAP" << std::endl;

                num_srcfiles           = hash_table->srcfiles.size();
                std::cout << " RESIZING HEAP TO " << num_srcfiles << std::endl;

                data.resize( num_srcfiles );
                rest.resize( num_srcfiles );


                std::cout << " ADDING FILES TO HEAP" << std::endl;
                for ( uint_t position = 0; position < num_srcfiles; ++position ) {
                    std::cout << " gettting heap num " << position << " / " << num_srcfiles << std::endl;

                    string_t infile = hash_table->srcfiles[ position ];

                    std::cout << " loading infile " << infile << " id " << position << std::endl;

                    data[ position ]    = new heapdata( infile );

                    std::cout << " printing" << std::endl;

                    data[ position ]->print();

                    std::cout << " printed" << std::endl;

                    std::cout << " kmer size of file " << infile << " = " << data[ position ]->get_kmer_size()  << std::endl;
                    std::cout << " finalhash of file " << infile << " = " << data[ position ]->get_final_hash() << std::endl;

                    if ( data[ position ]->get_final_hash() > finalhash ) {
                        finalhash = data[ position ]->get_final_hash();
                    }

                    if ( data[ position ]->get_last_hash() > lasthash ) {
                        lasthash = data[ position ]->get_last_hash();
                    }


                    if ( data[ position ]->get_kmer_size() == 0 ) {
                        std::cout << "kmer size of file " << infile << " == " << data[ position ]->get_kmer_size() << std::endl;
                        exit(1);
                    }

                    if ( get_kmer_size() != data[ position ]->get_kmer_size() ) {
                        std::cout << "kmer sizes differ: " << get_kmer_size() << " != " << data[ position ]->get_kmer_size() << std::endl;
                        exit(1);
                    }





                    std::cout << " loaded  infile " << infile << " id " << position << " kmer_size " << get_kmer_size() << " kmer_bytes " << get_kmer_bytes() << " data_bytes in " << get_data_bytes_in() << get_kmer_bytes() << " data_bytes out " << get_data_bytes_out() << " block_bytes in " << get_block_bytes_in() << " block_bytes out " << get_block_bytes_out() << " last hash " << get_final_hash() << std::endl;

                    num_infiles += data[ position ]->get_num_infiles();

                    std::cout << " cummulative num src files " << num_infiles << std::endl;
                }

                std::cout << " resizing resb to " << num_infiles << std::endl;
                resb.resize( num_infiles );

                std::cout << " FINISHED HEAP" << std::endl;
  }
}
namespace cnidaria
{
  bool jfheap::next ()
                        {
                                update();

                if ( numValid > 0 ) {
                                        return true;

                                } else {
                                        std::cout << "jfheap next has no valid" << std::endl;
                                        return false;

                                }
  }
}
namespace cnidaria
{
  bool jfheap::next (CNIDARIA_VAL_TYPE & r, baseInt & valid)
                                                                 {
                get( r, valid );

                return next();
  }
}
namespace cnidaria
{
  void jfheap::get (CNIDARIA_VAL_TYPE & r, baseInt & valid)
                                                                 {
                r     = resb;
                valid = numValid;
  }
}
namespace cnidaria
{
  void jfheap::getVec (CNIDARIA_VAL_TYPE & r)
                                                 {
                r     = resb;
  }
}
namespace cnidaria
{
  baseInt jfheap::getValid ()
                               {
                return numValid;
  }
}
namespace cnidaria
{
  void jfheap::update ()
                          {
                minH      = get_final_hash();
                numValid  = 0;

                resb.reset();
                rest.reset();


                for ( baseInt position = 0; position < num_srcfiles; ++position ) {

                    if ( data[position]->get_valid() ) {
                        baseInt tmp_hash = data[position]->get_hash();


                                                if ( ( lasthash != 0 ) && ( tmp_hash >= lasthash ) ) {
                                                        data[ position ]->set_valid( false );
                            rest[ position ] = false;

                                                } else if ( tmp_hash < minH ) {

                            rest.reset();
                            minH      = tmp_hash;
                            minMer    = data[position]->get_mer();
                            minKey    = data[position]->get_key();
                            rest[ position ] = true;

                        } else if ( tmp_hash == minH ) {





                            if ( data[position]->get_key() < minKey ) {

                                rest.reset();
                                minMer    = data[position]->get_mer();
                                minKey    = data[position]->get_key();
                                rest[ position ] = true;

                            } else if ( data[position]->get_key() == minKey ) {

                                rest[ position ] = true;
                            }
                        }
                    }
                }



                tmp_offset = 0;
                for ( baseInt position = 0; position < num_srcfiles; ++position ) {


                                        if ( data[ position ]->get_valid() ) {
                                                tmp_num_infiles = data[ position ]->get_num_infiles();


                                                if ( ( endhash != 0 ) && ( minH >= endhash ) ) {
                                                        data[ position ]->set_valid( false );


                                                } else if ( rest[ position ] ) {


                                                        tmp_res          = data[ position ]->get_val();

                                                        for ( baseInt offset = 0; offset < tmp_num_infiles; ++offset ) {
                                                                baseInt pos = tmp_offset + offset;



                                                                if ( tmp_res[ offset ] ) {
                                                                        ++hash_table->num_kmer_total_spp[ pos ];
                                                                        ++numValid;

                                                                        resb[ pos ] = tmp_res[ offset ];
                                                                }
                                                        }

                                                        if ( ! data[ position ]->next() ) {

                                                                data[ position ]->set_valid( false );
                                                        }
                                                } else {

                                                        tmp_res          = data[ position ]->get_val();








                                                }

                                                tmp_offset += tmp_num_infiles;
                                        }
                }
  }
}
namespace cnidaria
{
  void jfheap::seekHash (uint64_t req_hash)
                                               {
                for ( uint_t offset = 0; offset < num_srcfiles; ++offset ) {
                    string_t infile = hash_table->srcfiles[ offset ];
                    std::cout << " seeking " << req_hash << " in infile " << infile << " id " << (offset+1) << std::endl;
                    data[ offset ]->seekHash( req_hash );
                }
  }
}
namespace cnidaria
{
  progressBar merge_jfs::progressS;
}
namespace cnidaria
{
  baseInt merge_jfs::sCounter;
}
namespace cnidaria
{
  merge_jfs::merge_jfs (string_vec_t & srcfilesl, string_t basenamel)
    : srcfiles (srcfilesl), basename (basenamel), num_threads (1), num_pieces (1), piece_num (0), save_every (1), dump_every (10000000), gCounter (0), num_srcfiles (srcfiles.size()), kmer_size (0), kmer_bytes (0), data_bytes (0), block_bytes (0), export_complete (false), export_summary (false), export_matrix (true)
                {
                    init();
  }
}
namespace cnidaria
{
  void merge_jfs::init ()
                                                                     {
                progressS  = progressBar("Static Speed                    ", 0, pow(2,DEFAULT_MAX_DB_SIZE_EXPONENT));
                sCounter   = 0;
                hash_table = cnidaria_db( srcfiles, "cnidaria_db" );
                hda        = header_data();

                updateHeaderData();
  }
}
namespace cnidaria
{
  baseInt merge_jfs::get_complete_registers ()
                                                                                 { return hash_table.get_complete_registers();
  }
}
namespace cnidaria
{
  void merge_jfs::set_save_every (baseInt pe)
                                                                     { save_every = pe;
  }
}
namespace cnidaria
{
  void merge_jfs::set_num_pieces (baseInt np)
                                                                     { num_pieces = np;
  }
}
namespace cnidaria
{
  void merge_jfs::set_piece_num (baseInt pn)
                                                                     { piece_num  = pn;
  }
}
namespace cnidaria
{
  void merge_jfs::set_min_val (double mi)
                                                                     { hash_table.set_min_val( mi );
  }
}
namespace cnidaria
{
  void merge_jfs::set_max_val (double ma)
                                                                     { hash_table.set_max_val( ma );
  }
}
namespace cnidaria
{
  void merge_jfs::set_min_val (baseInt mi)
                                                                     { hash_table.set_min_val( mi );
  }
}
namespace cnidaria
{
  void merge_jfs::set_max_val (baseInt ma)
                                                                     { hash_table.set_max_val( ma );
  }
}
namespace cnidaria
{
  void merge_jfs::set_complete_registers (baseInt cr)
                                                                                 { hash_table.set_complete_registers( cr );
  }
}
namespace cnidaria
{
  void merge_jfs::append_complete_registers (baseInt cr)
                                                                                 { hash_table.set_complete_registers( get_complete_registers() + cr );
  }
}
namespace cnidaria
{
  void merge_jfs::set_export_summary (bool s)
                                                                     {                                                           hash_table.set_export_summary(       s           ); export_summary  = s;
  }
}
namespace cnidaria
{
  void merge_jfs::set_export_matrix (bool s)
                                                                     {                                                           hash_table.set_export_matrix(        s           ); export_matrix   = s;
  }
}
namespace cnidaria
{
  void merge_jfs::set_export_complete (bool s, string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.set_export_complete( hda, s, filename ); export_complete = s;
  }
}
namespace cnidaria
{
  void merge_jfs::enable_summary ()
                                                                     {                                                           hash_table.enable_summary();                        export_summary  = true;
  }
}
namespace cnidaria
{
  void merge_jfs::enable_matrix ()
                                                                     {                                                           hash_table.enable_matrix();                         export_matrix   = true;
  }
}
namespace cnidaria
{
  void merge_jfs::disable_summary ()
                                                                     {                                                           hash_table.disable_summary();                       export_summary  = false;
  }
}
namespace cnidaria
{
  void merge_jfs::disable_matrix ()
                                                                     {                                                           hash_table.disable_matrix();                        export_matrix   = false;
  }
}
namespace cnidaria
{
  void merge_jfs::disable_complete ()
                                                                     {                                                           hash_table.disable_complete();                      export_complete = false;
  }
}
namespace cnidaria
{
  void merge_jfs::enable_complete (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.enable_complete(     hda, filename );    export_complete = true;
  }
}
namespace cnidaria
{
  void merge_jfs::save_all (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.save_all(            hda, filename );
  }
}
namespace cnidaria
{
  void merge_jfs::load_all (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.load_all(            hda, filename );
  }
}
namespace cnidaria
{
  void merge_jfs::load (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.load(                hda, filename );
  }
}
namespace cnidaria
{
  void merge_jfs::save_summary (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.save_summary(        hda, filename );
  }
}
namespace cnidaria
{
  void merge_jfs::load_summary (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.load_summary(        hda, filename );
  }
}
namespace cnidaria
{
  void merge_jfs::save_matrix (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.save_matrix(         hda, filename );
  }
}
namespace cnidaria
{
  void merge_jfs::save_json_matrix (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.save_json_matrix(    hda, filename );
  }
}
namespace cnidaria
{
  void merge_jfs::load_matrix (string_t filename)
                                                                     { updateHeaderData(); if(filename==""){filename=basename;}; hash_table.load_matrix(         hda, filename );
  }
}
namespace cnidaria
{
  void merge_jfs::close_complete ()
                                                                     { updateHeaderData();                                       hash_table.close_complete(      hda           );
  }
}
namespace cnidaria
{
  void merge_jfs::set_num_threads (baseInt nt)
                                                                     {
                num_threads = nt;

                baseInt max_threads = get_max_threads();

                if ( num_threads > max_threads ) {
                    num_threads = max_threads;
                }
  }
}
namespace cnidaria
{
  void merge_jfs::updateHeaderData ()
                                                                     {
                hda.save_every  = save_every;
                hda.num_pieces  = num_pieces;
                hda.piece_num   = piece_num;
                hda.kmer_size   = kmer_size;
                hda.kmer_bytes  = kmer_bytes;
                hda.data_bytes  = data_bytes;
                hda.block_bytes = block_bytes;
  }
}
namespace cnidaria
{
  void merge_jfs::run (boost::recursive_mutex * g_guard_s)
                                                                     {
                updateHeaderData();

                std::cout << "starting phylogenomics with " << num_threads << " threads" << std::endl;
                std::cout << "starting " << num_threads << " threads" << std::endl;

                string_t    nameD     = (boost::format("DB Max Size  pc %3d/%3d         ") % (piece_num+1) % num_pieces).str();
                string_t    nameG     = (boost::format("Global Speed pc %3d/%3d         ") % (piece_num+1) % num_pieces).str();

                progressD = progressBar(nameD, 0, pow(2,DEFAULT_MAX_DB_SIZE_EXPONENT));
                progressG = progressBar(nameG, 0, pow(2,DEFAULT_MAX_DB_SIZE_EXPONENT));

                progressG.setProgress( false );
                progressS.setProgress( false );

                progressD.print( 1 );
                progressG.print( 1 );
                progressS.print( 1 );


                boost::recursive_mutex g_guard_m;
                boost::recursive_mutex g_guard_e;


                b_pool_t tp( num_threads );

                for ( baseInt threadNum = 0; threadNum < num_threads; ++threadNum ) {
                    tp.schedule(
                        boost::bind(
                            &merge_jfs::run_process, this, threadNum, g_guard_s, &g_guard_m, &g_guard_e
                        )
                    );
                }

                std::cout << "waiting for sub threads" << std::endl;
                tp.wait();
                std::cout << "sub threads finished "
                                          << "gCounter "               << gCounter << std::endl;
  }
}
namespace cnidaria
{
  void merge_jfs::run_process (baseInt const thread_num, boost::recursive_mutex * g_guard_s, boost::recursive_mutex * g_guard_m, boost::recursive_mutex * g_guard_e)
                                                                                                                                                                  {












                baseInt     num_threadsL   =   this->num_pieces * this->num_threads;
                baseInt     thread_numL    = ( this->piece_num  * this->num_threads ) + thread_num;

                string_t    name           = (boost::format("merge jfs pc %3d/%3d thr %3d/%3d") % (piece_num+1) % this->num_pieces % (thread_num + 1) % this->num_threads).str();

                std::cout << "CALLING HEAP with " << thread_numL << " threads out of " << num_threadsL << std::endl;
                jfheap      jfh( this->hash_table, num_threadsL, thread_numL, name );
                std::cout << "HEAP CALLED" << std::endl;

                baseInt     piecehash      = jfh.piecehash;
                baseInt     beginhash      = jfh.beginhash;
                baseInt     endhash        = jfh.endhash;
                baseInt     finalhash      = jfh.get_final_hash();
                baseInt     kmer_sizeL     = jfh.get_kmer_size();
                baseInt     kmer_bytesL    = jfh.get_kmer_bytes();
                baseInt     i_data_bytesL  = jfh.get_data_bytes_in();
                baseInt     o_data_bytesL  = jfh.get_data_bytes_out();
                baseInt     i_block_bytesL = jfh.get_block_bytes_in();
                baseInt     o_block_bytesL = jfh.get_block_bytes_out();
                baseInt     c              = 0;
                std::cout << "DATA GATHERED" << std::endl;

                                if ( beginhash > jfh.get_final_hash() ) {
                                        return;
                                }

                progressBar progress( name, beginhash, endhash );

                if ( g_guard_s != NULL ) { boost :: lock_guard < boost :: recursive_mutex > lock ( ( * g_guard_s ) ) ; } ;
                if ( this->kmer_size == 0 ) {
                    if ( kmer_sizeL == 0 ) {
                        std::cout << "kmer size is 0: " << kmer_sizeL << std::endl;
                        exit(1);

                    } else {
                        this->kmer_size   = kmer_sizeL;
                        this->kmer_bytes  = kmer_bytesL;
                        this->data_bytes  = o_data_bytesL;
                        this->block_bytes = o_block_bytesL;

                    }
                } else {
                    if ( this->kmer_size != kmer_sizeL ) {
                        std::cout << "kmer sizes differ: " << this->kmer_size << " != " << kmer_sizeL << std::endl;
                        exit(1);
                    }
                }
                if ( g_guard_s != NULL ) { boost :: lock_guard < boost :: recursive_mutex > unlock ( ( * g_guard_s ) ) ; } ;

                std::cout   << name << " finalhash       " << finalhash                  << "\n"
                            << name << " piecehash       " << piecehash                  << "\n"
                            << name << " beginhash       " << beginhash                  << "\n"
                            << name << " endhash         " << endhash                    << "\n"
                            << name << " kmer_size       " << kmer_sizeL                 << "\n"
                            << name << " kmer_bytes      " << kmer_bytesL                << "\n"
                            << name << " data_bytes in   " << i_data_bytesL              << "\n"
                            << name << " data_bytes out  " << o_data_bytesL              << "\n"
                            << name << " block_bytes in  " << i_block_bytesL             << "\n"
                            << name << " block_bytes out " << o_block_bytesL             << "\n"
                            << name << " num_pieces      " << this->num_pieces           << "\n"
                            << name << " piece_num       " << this->piece_num            << "\n"
                            << name << " num_threads     " << this->num_threads          << "\n"
                            << name << " thread_num      " << thread_num                 << "\n"
                            << name << " num_threadsG    " << num_threadsL               << "\n"
                            << name << " thread_numG     " << thread_numL                << "\n"

                            << name << " export_complete " << this->export_complete      << "\n"
                            << name << " export_summary  " << this->export_summary       << "\n"
                            << name << " export_matrix   " << this->export_matrix        << "\n"

                            << name << " save_every      " << this->save_every           << "\n"
                            << name << " dump_every      " << this->dump_every           << "\n"
                            << name << " min_val         " << this->hash_table.min_val_i << "\n"
                            << name << " max_val         " << this->hash_table.max_val_i << std::endl;

                progress.print( beginhash );


                while ( jfh.next() ) {
                    if ( g_guard_m != NULL ) { boost :: lock_guard < boost :: recursive_mutex > lock ( ( * g_guard_m ) ) ; } ;


                    if ( c % this->save_every == 0 ) {
                        if ( export_summary || export_matrix ) {
                            this->hash_table.add(  jfh.resb, jfh.numValid );
                            this->progressD.print( this->hash_table.hash_table.size() );
                        }
                    }




                    this->progressG.print( ++(*this).gCounter );

                    if ( this->export_complete ) {
                        register_data reg_data = { jfh.minH, jfh.minKey, jfh.resb, jfh.minMer, jfh.get_kmer_bytes(), jfh.get_data_bytes_out(), jfh.get_block_bytes_out() };

                        this->hash_table.serialize_complete_register( hda, reg_data );
                    }

                    progress.print( jfh.minH );

                    ++c;













                    this->progressS .print( ++(*this).sCounter );

                    if ( g_guard_m != NULL ) { boost :: lock_guard < boost :: recursive_mutex > unlock ( ( * g_guard_m ) ) ; } ;







                }
  }
}
namespace cnidaria
{
  void merge_jfs::merge (merge_jfs & merger)
                                                                     {
                merge( &merger );
  }
}
namespace cnidaria
{
  void merge_jfs::merge (merge_jfs * merger)
                                                                     {
                hash_table.merge( merger->hash_table );
  }
}
#undef LZZ_INLINE
