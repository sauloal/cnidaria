// cnidaria.cpp
//

#include "cnidaria.hpp"
#define LZZ_INLINE inline
int fact (int n)
                {
    if (n < 0){
        return 0;
    }
    if (n == 0) {
        return 1;
    }
    else {

        return n * fact(n-1);
    }
}
void version ()
               {
   std::cout   << "cnidaria version: " << __CNIDARIA_VERSION__ << "\n"
               << "build date      : " << "Sep 29 2015"        << "\n"
               << "build time      : " << "19:35:57"           << std::endl;
}
namespace cnidaria
{
  void openoutfile (std::ofstream & outfile_, string_t filename)
                                                                          {
        try {
            outfile_.open( filename, std::ios::out|std::ifstream::binary );
        } catch( std::ios_base::failure& e) {
            std::cerr << "Failed to open header of file '" << filename << "' Error: " << e.what() << std::endl;
            exit(1);
        }

        if (!outfile_.good()) {
            std::cout << "Failed to open header of file '" << filename << "' Error: " << std::strerror(errno) << "\n"
                      << "Failed to open header of file '" << filename << "' good : " << outfile_.good()      << "\n"
                      << "Failed to open header of file '" << filename << "' eof  : " << outfile_.eof()       << "\n"
                      << "Failed to open header of file '" << filename << "' fail : " << outfile_.fail()      << "\n"
                      << "Failed to open header of file '" << filename << "' bad  : " << outfile_.bad()       << std::endl;
            exit(1);
        }

        std::cout << "opened " << filename << std::endl;
  }
}
namespace cnidaria
{
  void openinfile (std::ifstream & infile_, string_t filename)
                                                                          {
        try {
            infile_.open( filename, std::ios::in|std::ifstream::binary );
        } catch( std::ios_base::failure& e) {
            std::cerr << "Failed to open header of file '" << filename << "' Error: " << e.what() << std::endl;
            exit(1);
        }

        if (!infile_.good()) {
            std::cout << "Failed to open header of file '" << filename << "' Error: " << std::strerror(errno) << "\n"
                      << "Failed to open header of file '" << filename << "' good : " << infile_.good()       << "\n"
                      << "Failed to open header of file '" << filename << "' eof  : " << infile_.eof()        << "\n"
                      << "Failed to open header of file '" << filename << "' fail : " << infile_.fail()       << "\n"
                      << "Failed to open header of file '" << filename << "' bad  : " << infile_.bad()        << std::endl;
            exit(1);
        }

        std::cout << "opened " << filename << std::endl;
  }
}
namespace cnidaria
{
  void merge_complete (string_t out_file, string_vec_t cfiles)
                                                                          {
        std::cout << "merge complete :: merging complete databases " << out_file << std::endl;

        std::ofstream oufile_;

        std::cout << "opening out file " << out_file + EXT_COMPLETE << std::endl;
        openoutfile( oufile_, out_file + EXT_COMPLETE );









        baseInt zero = 0;
        oufile_.write( reinterpret_cast<const char *>(&zero), sizeof(baseInt) );

        cnidaria_header_rw          hd_g = cnidaria_header_rw();
        header_data                 hda_g;

        string_vec_t                infiles_g;
        string_vec_t                srcfiles_g;
        tri_baseint_vec_t           matrix_g;
        hash_table_b_t              hash_table_g;
        baseint_vec_t               num_kmer_total_spp_g;
        baseint_vec_t               num_kmer_valid_spp_g;
        j_matrix_s_vec_t            j_matrices_g;

        hda_g.infiles            = &infiles_g;
        hda_g.srcfiles           = &srcfiles_g;
        hda_g.matrix             = &matrix_g;
        hda_g.hash_table         = &hash_table_g;
        hda_g.num_kmer_total_spp = &num_kmer_total_spp_g;
        hda_g.num_kmer_valid_spp = &num_kmer_valid_spp_g;
        hda_g.j_matrices         = &j_matrices_g;

        baseInt    fileCount     =  0;
        baseInt    sumRegisters  =  0;
        baseInt    sumRegistersD =  0;
        pos_type   sumDataSize   =  0;
        pos_type   startPos      =  oufile_.tellp();
        pos_type   lastDataPos   =  startPos;

        progressBar progressl1("merging complete files", 1, cfiles.size());

        for ( string_t infile: cfiles ) {
            std::cout << "infile " << infile << std::endl;

            std::ifstream infile_;

            openinfile( infile_, infile );






            std::cout << " parsing in file " << std::endl;

            cnidaria_header_rw  hd = cnidaria_header_rw ();
            header_data         hda;

            string_vec_t        infiles;
            string_vec_t        srcfiles;
            tri_baseint_vec_t   matrix;
            hash_table_b_t      hash_table;
            baseint_vec_t       num_kmer_total_spp;
            baseint_vec_t       num_kmer_valid_spp;
            j_matrix_s_vec_t    j_matrices;


            hda.infiles            = &infiles;
            hda.srcfiles           = &srcfiles;
            hda.matrix             = &matrix;
            hda.hash_table         = &hash_table;
            hda.num_kmer_total_spp = &num_kmer_total_spp;
            hda.num_kmer_valid_spp = &num_kmer_valid_spp;
            hda.j_matrices         = &j_matrices;


            std::cout << " loading header" << std::endl;
            hd.load_complete( hda, infile_ );
            std::cout << " printing header" << std::endl;
            hda.print();

            if ( fileCount == 0 ) {
                std::cout << " adding header" << std::endl;
                hda_g.add( hda );
                std::cout << " adding header :: result" << std::endl;
                hda_g.print();

            } else {
                std::cout << " merging header" << std::endl;
                hda_g.merge( hda );
                std::cout << " merged  header" << std::endl;

            }

            pos_type   json_pos       = hd.get_json_pos();



            baseInt    block_bytes    = hda.block_bytes;
            pos_type   data_size      = (pos_type)json_pos - (pos_type)sizeof(baseInt);
            baseInt    num_registers  = data_size / block_bytes;

            hd.copy_complete_registers( hda, json_pos, infile_, oufile_, fileCount, cfiles.size() );

            if ( num_registers != hda.complete_registers ) {
                std::cout << "number of found registers (" << num_registers << ") differ from number of expected registers (" << hda.complete_registers << ")" << std::endl;
                exit(1);
            }

            if ( ( data_size % block_bytes ) != 0 ) {
                std::cout << "data size " << data_size << " is not a multiple of block size " << block_bytes << std::endl;
                exit(1);
            }


            sumRegisters             += hda.complete_registers;
            sumRegistersD            += num_registers;
            sumDataSize              += data_size;

            pos_type endPos           = oufile_.tellp();
            pos_type data_size_o      = endPos - lastDataPos;

            if ( data_size_o != data_size ) {
                std::cout << " merging header :: error :: data size mistatch :: data_size_o: " << data_size_o << " data_size  : " << data_size   << std::endl;
                std::cout << " merging header :: error :: data size mistatch :: endPos     : " << endPos      << " lastDataPos: " << lastDataPos << std::endl;
                exit(1);

            }

            lastDataPos = endPos;

            ++fileCount;
            progressl1.print( fileCount );
        }

        std::cout << " final header" << std::endl;

        oufile_.flush();
        pos_type   json_pos      = oufile_.tellp();
        baseInt    num_srcfiles  = hda_g.num_srcfiles;
        baseInt    num_infiles   = hda_g.num_infiles;
        baseInt    kmer_bytes    = hda_g.kmer_bytes;
        baseInt    data_bytes    = hda_g.data_bytes;
        baseInt    block_bytes   = hda_g.block_bytes;
        pos_type   data_size     = (pos_type)json_pos  - (pos_type)sizeof(baseInt);
        baseInt    num_registers = data_size / block_bytes;

        std::cout << " final header :: num src files: " << num_srcfiles  << " num in files : " << num_infiles   << " kmer_bytes: " << kmer_bytes << " data_bytes  : " << data_bytes   << " block_bytes  : " << block_bytes   << std::endl;
        std::cout << " final header :: data_size    : " << data_size     << " num registers: " << num_registers << " json pos  : " << json_pos   << std::endl;

        if ( data_size % block_bytes != 0 ) {
            std::cout << " final header :: data size mismatch :: data size: " << data_size << " block size " << block_bytes << " remainder " << (data_size % block_bytes) << std::endl;
            exit(1);
        }

        std::cout << " final header :: num_registers: " << num_registers << " complete_registers: " << hda_g.complete_registers << " sumRegisters: " << sumRegisters << " sumRegistersD: " << sumRegistersD << std::endl;
        std::cout << " final header :: startPos     : " << startPos      << " sumDataSize       : " << sumDataSize              << " data_size   : " << data_size    << std::endl;

        if ( num_registers != hda_g.complete_registers ) {
            std::cout << " final header :: num registers mismatch :: theoretical: " << hda_g.complete_registers << " found: " << num_registers << " diff: " << (num_registers-hda_g.complete_registers) << std::endl;
            exit(1);
        }

        hda_g.num_pieces         = 1;
        hda_g.piece_num          = 0;
        hda_g.complete_registers = num_registers;
        hda_g.print();

        std::cout << " finished merging successfully. saving header" << std::endl;

        hd_g.save_header_complete_count( hda_g, oufile_ );

        std::cout << " finished merging successfully. closing file" << std::endl;

        oufile_.close();

        std::cout << " finished merging successfully. file closed" << std::endl;
  }
}
namespace cnidaria
{
  void merge_complete_parallel (string_t out_file, string_vec_t cfiles, baseInt num_threads)
                                                                                                          {
        std::cout << "merge complete :: merging complete databases " << out_file << std::endl;


        cnidaria_header_rw          hd_g = cnidaria_header_rw ();
        header_data                 hda_g;

        string_vec_t                infiles_g;
        string_vec_t                srcfiles_g;
        tri_baseint_vec_t           matrix_g;
        hash_table_b_t              hash_table_g;
        baseint_vec_t               num_kmer_total_spp_g;
        baseint_vec_t               num_kmer_valid_spp_g;
        j_matrix_s_vec_t            j_matrices_g;

        hda_g.infiles            = &infiles_g;
        hda_g.srcfiles           = &srcfiles_g;
        hda_g.matrix             = &matrix_g;
        hda_g.hash_table         = &hash_table_g;
        hda_g.num_kmer_total_spp = &num_kmer_total_spp_g;
        hda_g.num_kmer_valid_spp = &num_kmer_valid_spp_g;
        hda_g.j_matrices         = &j_matrices_g;

        baseInt    numCFiles     =  cfiles.size();
        baseInt    fileCount     =  0;
        baseInt    sumRegisters  =  0;
        baseInt    sumRegistersD =  0;
        pos_type   sumDataSize   =  0;
        std::vector<pos_type>starts;
        starts.resize( numCFiles );



        for ( string_t infile: cfiles ) {
            std::cout << "infile " << infile << std::endl;

            std::ifstream infile_;

            openinfile( infile_, infile );






            std::cout << " parsing in file " << std::endl;

            cnidaria_header_rw  hd = cnidaria_header_rw ();
            header_data         hda;

            string_vec_t        infiles;
            string_vec_t        srcfiles;
            tri_baseint_vec_t   matrix;
            hash_table_b_t      hash_table;
            baseint_vec_t       num_kmer_total_spp;
            baseint_vec_t       num_kmer_valid_spp;
            j_matrix_s_vec_t    j_matrices;


            hda.infiles            = &infiles;
            hda.srcfiles           = &srcfiles;
            hda.matrix             = &matrix;
            hda.hash_table         = &hash_table;
            hda.num_kmer_total_spp = &num_kmer_total_spp;
            hda.num_kmer_valid_spp = &num_kmer_valid_spp;
            hda.j_matrices         = &j_matrices;


            std::cout << " loading header" << std::endl;
            hd.load_complete( hda, infile_ );
            std::cout << " printing header" << std::endl;
            hda.print();

            if ( fileCount == 0 ) {
                std::cout << " adding header" << std::endl;
                hda_g.add( hda );
                std::cout << " adding header :: result" << std::endl;
                hda_g.print();

            } else {
                std::cout << " merging header" << std::endl;
                hda_g.merge( hda );
                std::cout << " merged  header" << std::endl;

            }

            pos_type   json_pos       = hd.get_json_pos();



            baseInt    block_bytes    = hda.block_bytes;
            pos_type   data_size      = (pos_type)json_pos - (pos_type)sizeof(baseInt);
            baseInt    num_registers  = data_size / block_bytes;

            if ( num_registers != hda.complete_registers ) {
                std::cout << "number of found registers (" << num_registers << ") differ from number of expected registers (" << hda.complete_registers << ")" << std::endl;
                exit(1);
            }

            if ( ( data_size % block_bytes ) != 0 ) {
                std::cout << "data size " << data_size << " is not a multiple of block size " << block_bytes << std::endl;
                exit(1);
            }

            starts[ fileCount ]       = sumDataSize;

            sumRegisters             += hda.complete_registers;
            sumRegistersD            += num_registers;

            sumDataSize              += data_size + std::streamoff( block_bytes );
            ++fileCount;
        }

        for ( baseInt fileCountN = 0; fileCountN < numCFiles; ++ fileCountN ) {
            std::cout << "file " << cfiles[fileCountN].c_str() << " from " << starts[fileCountN] << std::endl;
        }






        std::ofstream oufile_;

        std::cout << "opening out file " << out_file + EXT_COMPLETE << std::endl;
        openoutfile( oufile_, out_file + EXT_COMPLETE );








        std::cout << "opening out file " << out_file + EXT_COMPLETE << " :: writing zero" << std::endl;
        baseInt zero = 0;
        oufile_.write( reinterpret_cast<const char *>(&zero), sizeof(baseInt) );
        pos_type   startPos      =  oufile_.tellp();


        pos_type json_pos_t = sumDataSize + (pos_type)sizeof(baseInt);
        std::cout << "opening out file " << out_file + EXT_COMPLETE << " :: expanding" << std::endl;
        oufile_.seekp( json_pos_t );

        if ( json_pos_t != oufile_.tellp() ) {
            std::cout << "failed to seek end pos " << json_pos_t << " for output " << out_file << ". got pos " << oufile_.tellp() << std::endl;
            exit(1);
        }

        oufile_.write( reinterpret_cast<const char *>(&zero), sizeof(baseInt) );




















        b_pool_t tp( num_threads );

        fileCount     =  0;
        for ( string_t infile: cfiles ) {
            pos_type begin_pos = starts[fileCount] + (pos_type)sizeof(baseInt);

            tp.schedule(
                boost::bind(
                    &merge_complete_parallel_piece, out_file, numCFiles, fileCount, begin_pos, infile
                )
            );

            ++fileCount;
        }

        std::cout << "waiting for threads" << std::endl;
        tp.wait();






        std::cout << "opening out file " << out_file + EXT_COMPLETE << " :: seeking end" << std::endl;
        oufile_.seekp( json_pos_t );
        if ( json_pos_t != oufile_.tellp() ) {
            std::cout << "failed to seek end pos " << json_pos_t << " for output " << out_file << ". got pos " << oufile_.tellp() << std::endl;
            exit(1);
        }

        std::cout << "opening out file " << out_file + EXT_COMPLETE << " :: seeking end" << std::endl;
        baseInt    num_srcfiles  = hda_g.num_srcfiles;
        baseInt    num_infiles   = hda_g.num_infiles;
        baseInt    kmer_bytes    = hda_g.kmer_bytes;
        baseInt    data_bytes    = hda_g.data_bytes;
        baseInt    block_bytes   = hda_g.block_bytes;

        pos_type   json_pos      = oufile_.tellp();
        pos_type   data_size     = (pos_type)json_pos  - (pos_type)sizeof(baseInt);
        baseInt    num_registers = data_size / block_bytes;

        std::cout << " final header :: num src files: " << num_srcfiles  << " num in files : " << num_infiles   << " kmer_bytes: " << kmer_bytes << " data_bytes  : " << data_bytes   << " block_bytes  : " << block_bytes   << std::endl;
        std::cout << " final header :: data_size    : " << data_size     << " num registers: " << num_registers << " json pos  : " << json_pos   << std::endl;

        if ( data_size % block_bytes != 0 ) {
            std::cout << " final header :: data size mismatch :: data size: " << data_size << " block size " << block_bytes << " remainder " << (data_size % block_bytes) << std::endl;
            exit(1);
        }

        std::cout << " final header :: num_registers: " << num_registers << " complete_registers: " << hda_g.complete_registers << " sumRegisters: " << sumRegisters << " sumRegistersD: " << sumRegistersD << std::endl;
        std::cout << " final header :: startPos     : " << startPos      << " sumDataSize       : " << sumDataSize              << " data_size   : " << data_size    << std::endl;

        if ( num_registers != hda_g.complete_registers ) {
            std::cout << " final header :: num registers mismatch :: theoretical: " << hda_g.complete_registers << " found: " << num_registers << " diff: " << (num_registers-hda_g.complete_registers) << std::endl;
            exit(1);
        }

        hda_g.num_pieces         = 1;
        hda_g.piece_num          = 0;
        hda_g.complete_registers = num_registers;
        hda_g.print();

        std::cout << " finished merging successfully. saving header" << std::endl;

        hd_g.save_header_complete_count( hda_g, oufile_ );

        std::cout << " finished merging successfully. closing file" << std::endl;

        oufile_.close();

        std::cout << " finished merging successfully. file closed" << std::endl;
  }
}
namespace cnidaria
{
  void merge_complete_parallel_piece (string_t out_file, baseInt numCFiles, baseInt fileCount, pos_type begin_pos, string_t infile)
                                                                                                                                             {
        std::ofstream oufile_;

        std::cout << "opening out file " << out_file + EXT_COMPLETE << std::endl;
        openoutfile( oufile_, out_file + EXT_COMPLETE );








        oufile_.seekp( begin_pos );

        pos_type   startPos      =  oufile_.tellp();
        pos_type   lastDataPos   =  startPos;

        if ( startPos != begin_pos ) {
            std::cout << "failes to seek begin pos " << begin_pos << " for output " << out_file << " giving input " << infile << ". got pos " << startPos << std::endl;
            exit(1);
        }

        std::cout << "infile " << infile << std::endl;

        std::ifstream infile_;

        openinfile( infile_, infile );






        std::cout << " parsing in file " << std::endl;

        cnidaria_header_rw  hd = cnidaria_header_rw ();
        header_data         hda;

        string_vec_t        infiles;
        string_vec_t        srcfiles;
        tri_baseint_vec_t   matrix;
        hash_table_b_t      hash_table;
        baseint_vec_t       num_kmer_total_spp;
        baseint_vec_t       num_kmer_valid_spp;
        j_matrix_s_vec_t    j_matrices;
        baseInt             sumRegisters  =  0;


        hda.infiles            = &infiles;
        hda.srcfiles           = &srcfiles;
        hda.matrix             = &matrix;
        hda.hash_table         = &hash_table;
        hda.num_kmer_total_spp = &num_kmer_total_spp;
        hda.num_kmer_valid_spp = &num_kmer_valid_spp;
        hda.j_matrices         = &j_matrices;


        std::cout << " loading header" << std::endl;
        hd.load_complete( hda, infile_ );
        std::cout << " printing header" << std::endl;
        hda.print();


        pos_type   json_pos       = hd.get_json_pos();

        hd.copy_complete_registers( hda, json_pos, infile_, oufile_, fileCount, numCFiles );



        pos_type endPos           = oufile_.tellp();
        pos_type data_size        = (pos_type)json_pos - (pos_type)sizeof(baseInt);
        pos_type data_size_o      = endPos - lastDataPos;

        if ( data_size_o != data_size ) {
            std::cout << " merging header :: error :: data size mistatch :: data_size_o: " << data_size_o << " data_size  : " << data_size   << std::endl;
            std::cout << " merging header :: error :: data size mistatch :: endPos     : " << endPos      << " lastDataPos: " << lastDataPos << std::endl;
            exit(1);
        }
  }
}
namespace cnidaria
{
  void merge_matrix (string_t out_file, string_vec_t cfiles)
                                                                          {
        std::cout << "merge matrix :: merging matrix databases " << out_file << std::endl;

        progressBar progressl1("merge matrix", 0, 1000);
        progressl1.print( 1 );

        std::ofstream oufile_;

        std::cout << "opening out file " << out_file + EXT_MATRIX << std::endl;
        openoutfile( oufile_, out_file + EXT_MATRIX );

        cnidaria_header_rw          hd_g = cnidaria_header_rw ();
        header_data                 hda_g;

        string_vec_t                infiles_g;
        string_vec_t                srcfiles_g;
        tri_baseint_vec_t           matrix_g;
        hash_table_b_t              hash_table_g;
        baseint_vec_t               num_kmer_total_spp_g;
        baseint_vec_t               num_kmer_valid_spp_g;
        j_matrix_s_vec_t            j_matrices_g;

        hda_g.infiles            = &infiles_g;
        hda_g.srcfiles           = &srcfiles_g;
        hda_g.matrix             = &matrix_g;
        hda_g.hash_table         = &hash_table_g;
        hda_g.num_kmer_total_spp = &num_kmer_total_spp_g;
        hda_g.num_kmer_valid_spp = &num_kmer_valid_spp_g;
        hda_g.j_matrices         = &j_matrices_g;
        baseInt fileCount        =  0;

        for ( string_t infile: cfiles ) {
            std::cout << "infile " << infile << std::endl;

            std::ifstream infile_;

            openinfile( infile_, infile );

            std::cout << " parsing in file " << std::endl;

            header_data hda;
            cnidaria_header_rw        hd = cnidaria_header_rw ();

            string_vec_t              infiles;
            string_vec_t              srcfiles;
            tri_baseint_vec_t         matrix;
            hash_table_b_t            hash_table;
            baseint_vec_t             num_kmer_total_spp;
            baseint_vec_t             num_kmer_valid_spp;
            j_matrix_s_vec_t          j_matrices;

            hda.infiles            = &infiles;
            hda.srcfiles           = &srcfiles;
            hda.matrix             = &matrix;
            hda.hash_table         = &hash_table;
            hda.num_kmer_total_spp = &num_kmer_total_spp;
            hda.num_kmer_valid_spp = &num_kmer_valid_spp;
            hda.j_matrices         = &j_matrices;

            std::cout << " loading header" << std::endl;
            hd.load_matrix( hda, infile_ );
            std::cout << " printing header" << std::endl;


            if ( fileCount == 0 ) {
                std::cout << " adding header" << std::endl;
                hda_g.add( hda );
                std::cout << " adding header :: result" << std::endl;
                hda_g.print();

            } else {
                std::cout << " merging header" << std::endl;
                hda_g.merge( hda );
                std::cout << " merged  header" << std::endl;

            }

            ++fileCount;
        }

        std::cout << " final header" << std::endl;

        oufile_.flush();

        hda_g.num_pieces = 1;
        hda_g.piece_num  = 0;
        hda_g.print();

        std::cout << " finished merging successfully. saving header" << std::endl;

        hd_g.save_matrix( hda_g, oufile_ );

        std::cout << " finished merging successfully. closing file" << std::endl;

        oufile_.close();

        std::cout << " finished merging successfully. file closed" << std::endl;
  }
}
namespace cnidaria
{
  void merge_matrixj (string_t out_file, string_vec_t cfiles)
                                                                          {
        std::cout << "merge matrix json :: merging matrix json databases " << out_file << std::endl;

        progressBar progressl1("merge matrix json", 0, 1000);
        progressl1.print( 1 );

        std::ofstream oufile_;

        std::cout << "opening out file " << out_file + EXT_JMATRIX << std::endl;
        openoutfile( oufile_, out_file + EXT_JMATRIX );

        cnidaria_header_rw          hd_g = cnidaria_header_rw ();
        header_data                 hda_g;

        string_vec_t                infiles_g;
        string_vec_t                srcfiles_g;
        tri_baseint_vec_t           matrix_g;
        hash_table_b_t              hash_table_g;
        baseint_vec_t               num_kmer_total_spp_g;
        baseint_vec_t               num_kmer_valid_spp_g;
        j_matrix_s_vec_t            j_matrices_g;

        hda_g.infiles            = &infiles_g;
        hda_g.srcfiles           = &srcfiles_g;
        hda_g.matrix             = &matrix_g;
        hda_g.hash_table         = &hash_table_g;
        hda_g.num_kmer_total_spp = &num_kmer_total_spp_g;
        hda_g.num_kmer_valid_spp = &num_kmer_valid_spp_g;
        hda_g.j_matrices         = &j_matrices_g;

        baseInt fileCount     = 0;

        for ( string_t infile: cfiles ) {
            std::cout << "infile " << infile << std::endl;

            std::ifstream infile_;

            openinfile( infile_, infile );

            std::cout << " parsing in file " << infile << std::endl;

            header_data hda;
            cnidaria_header_rw        hd = cnidaria_header_rw ();

            string_vec_t              infiles;
            string_vec_t              srcfiles;
            tri_baseint_vec_t         matrix;
            hash_table_b_t            hash_table;
            baseint_vec_t             num_kmer_total_spp;
            baseint_vec_t             num_kmer_valid_spp;
            j_matrix_s_vec_t          j_matrices;

            hda.infiles            = &infiles;
            hda.srcfiles           = &srcfiles;
            hda.matrix             = &matrix;
            hda.hash_table         = &hash_table;
            hda.num_kmer_total_spp = &num_kmer_total_spp;
            hda.num_kmer_valid_spp = &num_kmer_valid_spp;
            hda.j_matrices         = &j_matrices;

            std::cout << " loading header" << std::endl;
            hd.load_jmatrix( hda, infile_ );
            std::cout << " printing header" << std::endl;
            hda.print();

            if ( fileCount == 0 ) {
                std::cout << " adding header" << std::endl;
                hda_g.add( hda );
                std::cout << " adding header :: result" << std::endl;
                hda_g.print();

            } else {
                std::cout << " merging header" << std::endl;
                hda_g.merge( hda );
                std::cout << " merged  header" << std::endl;

            }

            ++fileCount;
        }

        std::cout << " final header" << std::endl;

        hda_g.num_pieces = 1;
        hda_g.piece_num  = 0;
        hda_g.print();

        hd_g.save_header_json_matrix( hda_g, oufile_ );

        std::cout << " finished merging successfully. closing file" << std::endl;

        oufile_.close();

        std::cout << " finished merging successfully. file closed" << std::endl;
  }
}
namespace cnidaria
{
  piece_data::piece_data (string_vec_t & srcfiles_, string_t & out_file_, baseInt num_threads_, baseInt minVal_, baseInt save_every_, bool export_complete_, bool export_summary_, bool export_matrix_, baseInt num_pieces_, baseInt piece_num_)
    : srcfiles (srcfiles_), out_file (out_file_), num_threads (num_threads_), minVal (minVal_), save_every (save_every_), export_complete (export_complete_), export_summary (export_summary_), export_matrix (export_matrix_), num_pieces (num_pieces_), piece_num (piece_num_)
                {
                    merger = new merge_jfs( srcfiles_, out_file_ );
                    locker = new boost::recursive_mutex;
  }
}
namespace cnidaria
{
  void send_pieces (piece_data_vec_t data)
                                              {
        b_pool_t tp( data.size() );

        for ( baseInt piece_num = 0; piece_num < data.size(); ++piece_num ) {
            std::cout << "sending thread " << piece_num << " out of " << data.size() << std::endl;
            tp.schedule(
                boost::bind(
                    &send_piece, data[piece_num]
                )
            );
        }

        std::cout << "waiting for threads" << std::endl;
        tp.wait();
        std::cout << "threads finished" << std::endl;
        std::cout << "sent all pieces"  << std::endl;
        for ( baseInt piece_num = 0; piece_num < data.size(); ++piece_num ) {
            std::cout   << "piece"    << piece_num << " = "
                        << "gCounter" << data[piece_num].merger->get_complete_registers() << std::endl;
        }
  }
}
namespace cnidaria
{
  void send_piece (piece_data data)
                                              {


        data.merger->enable_summary();
        data.merger->enable_matrix();

        data.merger->set_num_threads(     data.num_threads     );
        data.merger->set_num_pieces(      data.num_pieces      );
        data.merger->set_piece_num(       data.piece_num       );
        data.merger->set_min_val(         data.minVal          );
        data.merger->set_save_every(      data.save_every      );
        data.merger->set_export_complete( data.export_complete );
        data.merger->set_export_summary(  data.export_summary  );
        data.merger->set_export_matrix(   data.export_matrix   );

        data.merger->run( data.locker );

        std::cout   << "piece sent gCounter: " << data.merger->get_complete_registers() << std::endl;
  }
}
namespace cnidaria
{
  void send_data (string_vec_t srcfiles, string_t out_file, baseInt num_threads, baseInt minVal, baseInt save_every, bool export_complete, bool export_summary, bool export_matrix, baseInt num_pieces, baseInt piece_num)
              {
        piece_data d    = piece_data( srcfiles, out_file, num_threads, minVal, save_every, export_complete, export_summary, export_matrix, num_pieces, piece_num );

        send_piece( d );

        std::cout   << "saving" << std::endl;
        std::cout   << "data sent gCounter: " << d.merger->get_complete_registers() << std::endl;

        d.merger->save_all( out_file );
  }
}
namespace cnidaria
{
  void merge_data (string_t out_file, string_vec_t srcfiles_complete, string_vec_t srcfiles_matrix, string_vec_t srcfiles_matrixj, bool do_merge_complete, bool do_merge_matrix)
                                                                                                                                                                                    {
        if ( do_merge_complete ) {
            merge_complete( out_file, srcfiles_complete );

        }

        if ( do_merge_matrix ) {
            merge_matrix(   out_file, srcfiles_matrix   );
            merge_matrixj(  out_file, srcfiles_matrixj  );
        }
  }
}
namespace cnidaria
{
  void dump (string_vec_t infiles)
                                      {
        for ( string_t infile: infiles ) {
            dump( infile );
        }
  }
}
namespace cnidaria
{
  void dump (string_t infile)
                                 {
        typedef  jelly::jelly_iterator  j_file_iterator_t;
        std::cout << "Dumping " << infile << std::endl;
        j_file_iterator_t *it = new j_file_iterator_t( infile );
        it->dump();
  }
}
#undef LZZ_INLINE
