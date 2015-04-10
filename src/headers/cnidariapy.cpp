#include <stdint.h>

#include <boost/python.hpp>
#include <boost/python/raw_function.hpp>
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/args.hpp>
#include <boost/python/tuple.hpp>
#include <boost/python/class.hpp>
#include <boost/python/overloads.hpp>
#include <boost/python/return_internal_reference.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

#include "cnidaria.hpp"

typedef std::string                         string_t;
typedef unsigned int                        uint_t;

typedef boost::python::str                  p_string_t;
typedef boost::python::tuple                p_tuple_t;
typedef boost::python::dict                 p_dict_t;
typedef boost::python::list                 p_list_t;
typedef boost::python::long_                p_long_t;
typedef boost::python::ssize_t              p_size_t;
typedef boost::python::object               p_object_t;

//typedef cnidaria::phylogenomics_t           phylogenomics_t;
//typedef cnidaria::header_t                  header_t;
//typedef cnidaria::hash_table_v_t            hash_table_v_t;
//typedef cnidaria::string_vec_t              string_vec_t;
//typedef cnidaria::baseInt                   baseInt;


/*
template <class T>
boost::python::list toPythonList(std::vector<T> vector) {
	typename std::vector<T>::iterator iter;
	boost::python::list list;
	for (iter = vector.begin(); iter != vector.end(); ++iter) {
		list.append(*iter);
	}
	return list;
}
*/






/*
namespace cnidaria
{
  void openoutfile (std::ofstream & outfile_, string_t filename);

  void openinfile (std::ifstream & infile_, string_t filename);

  void merge_complete (string_t out_file, string_vec_t cfiles);

  void merge_complete_parallel (string_t out_file, string_vec_t cfiles, baseInt num_threads = 5);

  void merge_complete_parallel_piece (string_t out_file, baseInt numCFiles, baseInt fileCount, pos_type begin_pos, string_t infile);

  void merge_matrix (string_t out_file, string_vec_t cfiles);

  void merge_matrixj (string_t out_file, string_vec_t cfiles);

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
    piece_data (string_vec_t & srcfiles_, string_t & out_file_, baseInt num_threads_, baseInt minVal_, baseInt save_every_, bool export_complete_, bool export_summary_, bool export_matrix_, baseInt num_pieces_, baseInt piece_num_, merge_jfs * merger_, boost::recursive_mutex * locker_);
  };

  typedef std::vector <piece_data> piece_data_vec_t;

  void send_pieces (piece_data_vec_t data);

  void send_piece (piece_data data);
}






    void run_test_pieces(       string_vec_t srcfiles, string_t out_file, uint_t num_pieces, uint_t piece_num ) {
        if ( piece_num == num_pieces+1 ) {
            run_test_pieces_merge(           out_file, num_pieces );
        } else {
            run_test_pieces_split( srcfiles, out_file, num_pieces, piece_num );
        }
    }

    void run_test_pieces_merge( string_t out_file, uint_t num_pieces ) {
        std::cout << out_file << " merge" << std::endl;
        
        string_vec_t srcfiles_complete;
        string_vec_t srcfiles_matrix;
        string_vec_t srcfiles_matrixj;
        
        for ( uint_t piece_num = 0; piece_num < num_pieces; ++piece_num ) {
            string_t name_complete = (boost::format("%s_%04d_%04d%s") % out_file % piece_num % num_pieces % EXT_COMPLETE).str();
            std::cout << "adding " << name_complete << " to merging" << std::endl;
            srcfiles_complete.push_back( name_complete );
            
            string_t name_matrix = (boost::format("%s_%04d_%04d%s") % out_file % piece_num % num_pieces % EXT_MATRIX    ).str();
            std::cout << "adding " << name_matrix << " to merging" << std::endl;
            srcfiles_matrix.push_back( name_matrix );
            
            string_t name_matrixj = (boost::format("%s_%04d_%04d%s") % out_file % piece_num % num_pieces % EXT_JMATRIX  ).str();
            std::cout << "adding " << name_matrixj << " to merging" << std::endl;
            srcfiles_matrixj.push_back( name_matrixj );
        }
        
        merge_complete( out_file, srcfiles_complete );
        //merge_complete_parallel( out_file, srcfiles_complete );
        merge_matrix(   out_file, srcfiles_matrix   );
        merge_matrixj(  out_file, srcfiles_matrixj  );
    }
    
    void run_test_pieces_split( string_vec_t srcfiles, string_t out_file, uint_t num_pieces, uint_t piece_num ) {
        std::cout << out_file << std::endl;
        std::cout << out_file << " :: reading jf test 2" << std::endl;
        progressBar progressl1("read jf " + out_file, 0, 1000);
        progressl1.print( 1 );

        baseInt  num_threads     =   1;
        baseInt  minVal          =   2;
        baseInt  save_every      =   1;
        //baseInt  save_every      =   100000;
        bool     export_complete =  true;
        bool     export_summary  = false;
        bool     export_matrix   =  true;
        boost::recursive_mutex g_guard_s;

        
        piece_data_vec_t pieces;
        
        string_t   name = (boost::format("%s_%04d_%04d") % out_file % piece_num % num_pieces).str();
        
        piece_data d    = piece_data( srcfiles, name, num_threads, minVal, save_every, export_complete, export_summary, export_matrix, num_pieces, piece_num, new merge_jfs( srcfiles, name ), &g_guard_s );
        
        send_piece( d );
        
        progressl1.print( 500 );

        std::cout << out_file << " :: exporting" << std::endl;

        d.merger->save_all( name );
        
        progressl1.print( 1000 );

        std::cout << out_file << " :: read jf test 2 FINISHED" << std::endl;
    }




    void test1( uint_t num_pieces, uint_t piece_num ) {
        string_vec_t srcfiles;
        string_t     outfile = "test1";
        
        {
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_lyrata.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Arabidopsis_thaliana_TAIR10_genome.fas.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Citrus_sinensis.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Glycine_max.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Malus_domestica.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Nicotiana_benthamiana_Niben.genome.v0.4.4.scaffolds.nrcontigs.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Nicotiana_tabacum_tobacco_genome_sequences_assembly.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Oryza_brachyantha.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Oryza_sativa_build_5.00_IRGSPb5.fa.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Populus_trichocarpa.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/S_lycopersicum_chromosomes.2.40.fa.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_peruvianum_Speru_denovo.fa.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Solanum_tuberosum_PGSC_DM_v3_superscaffolds.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Spimpinellifolium_genome.contigs.fasta.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Vitis_vinifera_Genoscope_12X_2010_02_12_scaffolds.fa.31.jf" );
            srcfiles.push_back( "/mnt/scratch/aflit001/nobackup/phylogenomics_raw/external/Plants/Zea_mays.fasta.31.jf" );
        }
        
        run_test_pieces( srcfiles, outfile, num_pieces, piece_num );
        //run_test_single( srcfiles, outfile );
    }

    
    test_num   = atoi(argv[1]);
    num_pieces = atoi(argv[2]);
    piece_num  = atoi(argv[3]);
    
    cnidaria::test1( num_pieces, piece_num );


*/

class cnidariapy {
    public:
        cnidariapy(){}
        
}

/*
class cnidariapy {
    public:
        cnidariapy(){}
        
        void merge_jfs( const p_list_t &p_infilesl, const string_t &outfile, const baseInt threadsl=1, const baseInt binomialSample=0 ) {
            uint_t threads = threadsl;
            
            baseInt max_threads = cnidaria::get_max_threads();
            if ( threads > max_threads ) {
                threads = max_threads;
            }
            
            string_vec_t infiles;
            for ( uint_t s = 0; s < boost::python::len(p_infilesl); ++s ) {
                boost::python::extract<string_t> x( p_infilesl[ s ] );
                
                if( x.check() ) {
                    string_t v = x();
                    std::cout << "adding " << s << " v " << v << std::endl;
                    infiles.push_back( v );
                }
            };
            
            std::cout << "reading jfs" << std::endl;
            hash_table_v_t hash_table;
            cnidaria::merge_jfs_thr( hash_table, infiles, threads );
            std::cout << "read jfs" << std::endl;
            
            
            //std::cout << "saving bin" << std::endl;
            //phym.save( outfile );
            //std::cout << "saved bin" << std::endl;
        }
        
        void merge_dbs() {
            //std::cout << "TEST2 :: reading bin" << std::endl;
            //progressBar progressl3("saving bin", 0, 1000);
            //header_t h = header_t();
            //phylogenomics_t phyb = h.load( outfile );
            //progressl3.print( 1000 );
            //std::cout << "TEST2 :: read bin" << std::endl;
        }
};
*/

BOOST_PYTHON_MODULE(cnidariapy)
{
    boost::python::class_<cnidariapy>("cnidariapy")
        .def( "merge_jfs", &cnidariapy::merge_jfs )
        .def( "merge_dbs", &cnidariapy::merge_dbs )
    ;
}
