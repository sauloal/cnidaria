%module cnidariapy
%include "std_string.i"
%include "std_vector.i"

namespace std {
   %template(vectors) vector<string>;
   //%template(vectori) vector<int>;
   //%template(vectord) vector<double>;
};

%{
/* Includes the header in the wrapper code */
#include "shared.hpp"
#include "cnidaria.hpp"

using namespace cnidaria;
%}

%include shared.hpp
%include cnidaria.hpp
//using namespace cnidaria;


