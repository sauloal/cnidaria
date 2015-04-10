
col_names_debug_matrix_data     <- c("filename",    "col_name", "status",           "query_name",              "query_class",            "query_index",               "hit_index_min",              "hit_value_min",                 "hit_name_min",                                                   "hit_index_min_values",                      "hit_class_min", "res")
len_col_names_debug_matrix_data <- length(col_names_debug_matrix_data)  





nearest_neighbour_classifier <- function(json_file, json_data, classes_file, polytomy_handler=NA) {
  classes_data <- read.csv(classes_file, sep="\t", strip.white=T, blank.lines.skip=T, skipNul=T, header=T, stringsAsFactors=T)
  classes_data <- classes_data[ classes_data$Sample != "" & classes_data$Use == 1,       ]
  #   print(classes_data)

  classes_data_row_names <- classes_data[,1]
  classes_data_col_names <- colnames(classes_data)
  classes_data_col_names <- classes_data_col_names[-which(classes_data_col_names %in% c("Sample", "Use"))]
  
  print("length(classes_data_row_names)")
  print(length(classes_data_row_names))
  print("classes_data_row_names")
  print(classes_data_row_names)

  print("length(classes_data_col_names)")
  print(length(classes_data_col_names))
  print("classes_data_col_names")
  print(classes_data_col_names)

  distance          <- json_data$matrix_distance
  distance_rownames <- rownames(distance)
#   print("distance_rownames")
#   print(distance_rownames)

  #distance_coords   <- unlist(sapply(classes_data_row_names, function(x) { which(distance_rownames == x, arr.ind=T) } ))
  distance_coords   <- distance_rownames %in% classes_data_row_names
  print("sum(distance_coords)")
  print(sum(distance_coords))  
  print("sum(!distance_coords)")
  print(sum(!distance_coords))

  print("deleting from matrix")
  print(distance_rownames[!distance_coords])
  
  print(paste("length(distance_coords)",length(distance_coords)))
  distance          <- distance[ distance_coords, distance_coords ]

  print(paste("length(distance[1,])", length(distance[1,])))
  distance_rownames <- rownames(distance)

  print( "distance_rownames" )
  print( distance_rownames   )

  print( "length(distance_rownames)" )
  print( length(distance_rownames)   )


  classes_data_coords       <- classes_data_row_names %in% distance_rownames
  print("sum(classes_data_coords)")
  print(sum(classes_data_coords))  
  print("sum(!classes_data_coords)")
  print(sum(!classes_data_coords))


  classes_data              <- classes_data[classes_data_coords,]
  classes_data_row_names    <- classes_data[,1]

  print("length(classes_data_row_names)")
  print(length(classes_data_row_names))
  print("classes_data_row_names")
  print(classes_data_row_names)

  print("classes_data")
  print(classes_data)


  out_lst <- paste(classes_file, '.lst', sep="")
  print(paste("saving log to", out_lst))
  write.table(classes_data_row_names, file=out_lst, sep="\t", na="", quote=F, row.names=F)


  


  debug_matrix_data               <- matrix(,nrow=0,ncol=len_col_names_debug_matrix_data)
  colnames(debug_matrix_data)     <- col_names_debug_matrix_data
  

  print("debug_matrix_data INIT")
  print(debug_matrix_data)





  filter_l    <- function(name, class_data, x) {
    print(paste("filtering", name))

    data_names   <- class_data[ ,1]
    data_classes <- class_data[ ,2]
    query_name   <- class_data[x,1]
    query_class  <- class_data[x,2]
    query_index  <- which(distance_rownames==query_name, arr.ind=T)
    print(paste("query_name", query_name, "query_class", query_class))
    
    if (length(query_index) > 0) {
      distance_row <- distance[query_index,]
      sorted_row   <- sort(distance_row, decreasing=F, index.return=F, method = "shell")
      sorted_row   <- order(distance_row)

      if (F) {
        print("distance_row")
        print(distance_row)
        print("sorted_row")
        print(sorted_row)
        print(distance_row[sorted_row])
      }
      
      for (h in 1:length(distance_row)) {
        hit_index_min        <- sorted_row[h]
        hit_value_min        <- distance_row[hit_index_min]
        
        if (is.na(hit_value_min)) {
          next()
        }
        
        hit_index_min_values <- which(unlist(distance_row)==hit_value_min, arr.ind=T)
        hit_names_min        <- distance_rownames[hit_index_min_values]
        num_min              <- length(hit_index_min_values)
        
        if (F) {
          print("h")
          print(h)
          print("hit_index_min")
          print(hit_index_min)
          print("hit_value_min")
          print(hit_value_min)
          print("hit_index_min_values")
          print(hit_index_min_values)
          print("hit_names_min")
          print(hit_names_min)
          print("num_min")
          print(num_min)
        }
        
        if      ( num_min == 0 ) {
          print(paste("  NO MIN         file", json_file, "name",                 name,"x",x,"query_name",  query_name, "query_class",  query_class,"query_index",query_index,"h",h,"hit_index_min",hit_index_min,"hit_value_min",hit_value_min,"h_name_min",NA                 ,"hit_index_min_values",NA                                                ,                               "res",   NA))
          row_data           <- matrix(c(json_file,   toString(name), "NO MIN", toString(query_name),       toString(query_class),             query_index,                      hit_index_min,                hit_value_min,             NA                 ,                       NA                                                ,                      NA,               NA), nrow=1, ncol=len_col_names_debug_matrix_data, byrow=T)
          #                              "filename",      "col_name", "status",         "query_name",               "query_class",            "query_index",                    "hit_index_min",              "hit_value_min",                 "hit_name_min",                                                   "hit_index_min_values",                      "hit_class_min", "res"
          debug_matrix_data <<- rbind(debug_matrix_data, row_data)
          next()
        }
        else if ( num_min  > 1 ) {
          print(paste("  MULTIPLE BEGIN file", json_file, "name",    name,"x",x,"query_name",          query_name, "query_class",  query_class,"query_index",query_index,"h",h,"hit_index_min",hit_index_min,"hit_value_min",hit_value_min,"h_name_min",paste(hit_names_min, sep="", collapse=","),"hit_index_min_values",paste(hit_index_min_values, sep="", collapse=","),           "res",NA))
          row_data           <- matrix(      c(json_file,   toString(name), "MULTIPLE BEGIN", toString(query_name),       toString(query_class),             query_index,                      hit_index_min,                hit_value_min,             paste(hit_names_min, sep="", collapse=","),                       paste(hit_index_min_values, sep="", collapse=","), NA,             NA), nrow=1, ncol=len_col_names_debug_matrix_data, byrow=T)
          #                                   "filename",       "col_name", "status",                 "query_name",               "query_class",            "query_index",                    "hit_index_min",              "hit_value_min",                 "hit_name_min",                                                   "hit_index_min_values",                      "hit_class_min", "res"
          debug_matrix_data <<- rbind(debug_matrix_data, row_data)
          
          
          
          if ( is.na(polytomy_handler) ) {
            print(paste("  MULTIPLE END file", json_file, "name",name,"x",x,"query_name",         query_name, "query_class",   query_class,"query_index",query_index,"h",h,"hit_index_min",hit_index_min,"hit_value_min",hit_value_min,"h_name_min",paste(hit_names_min, sep="", collapse=","),"hit_index_min_values",paste(hit_index_min_values, sep="", collapse=","),           "res",NA))
            row_data           <- matrix(    c(json_file, toString(name), "MULTIPLE END", toString(query_name),       toString(query_class),             query_index,                      hit_index_min,                hit_value_min,             paste(hit_names_min, sep="", collapse=","),                       paste(hit_index_min_values, sep="", collapse=","), NA,             NA), nrow=1, ncol=len_col_names_debug_matrix_data, byrow=T)
            #                                 "filename",     "col_name", "status",               "query_name",               "query_class",            "query_index",                    "hit_index_min",              "hit_value_min",                 "hit_name_min",                                                   "hit_index_min_values",                      "hit_class_min", "res"
            debug_matrix_data <<- rbind(debug_matrix_data, row_data)
            return(NA)
          }
          
          
          
          mult_found   <- c()
          for ( hit_index_min_v in hit_index_min_values ) {
            hit_value_min_v <- distance_row[hit_index_min_v]
            hit_names_min_v <- distance_rownames[hit_index_min_v]

            if ( query_index == hit_index_min_v ) {
              print(paste("SAME QUERY INDEX", query_index, hit_index_min_v))
              next()
            }
            
            if ( ! ( hit_names_min_v %in% data_names ) )  {
              print(paste("HIT NOT IN NAMES", hit_names_min_v))
#               print(data_names)
              next()
            }
            
            hit_class_min_i <- which(data_names==hit_names_min_v, arr.ind=T)
            hit_class_min_v <- data_classes[hit_class_min_i]
            
            res <- (query_class == hit_class_min_v)
            
            print(paste("  MULTIPLE ROW file", json_file, "name",  name,"x",x,"query_name",        query_name, "query_class",  query_class,"query_index",query_index,"h",h,"hit_index_min",hit_index_min_v,"hit_value_min",hit_value_min_v,"h_name_min",paste(hit_names_min_v, sep="", collapse=","),"hit_index_min_values",hit_index_min_v, "hit_class_min", toString(hit_class_min_v), "res",res))
            row_data           <- matrix(c(    json_file, toString(name), "MULTIPLE ROW", toString(query_name),       toString(query_class),             query_index,                      hit_index_min_v,                hit_value_min_v,             paste(hit_names_min_v, sep="", collapse=","),                       hit_index_min_v,                  toString(hit_class_min_v),       res), nrow=1, ncol=len_col_names_debug_matrix_data, byrow=T)
            #                                 "filename",     "col_name", "status",               "query_name",               "query_class",            "query_index",                    "hit_index_min",                "hit_value_min",                   "hit_name_min",                                              "hit_index_min_values",                     "hit_class_min",        "res"
            debug_matrix_data <<- rbind(debug_matrix_data, row_data)
            
            mult_found <- c( mult_found, res )
          }
          

          if ( length(mult_found) == 0 ) {
            print(" going to next value")
            print(paste("  MULTIPLE END file", json_file, "name",                 name,"x",x,"query_name",        query_name, "query_class",  query_class,"query_index",query_index,"h",h,"hit_index_min",hit_index_min,"hit_value_min",hit_value_min,"h_name_min",paste(hit_names_min, sep="", collapse=","),"hit_index_min_values",paste(hit_index_min_values, sep="", collapse=","),                 "res", NA))
            row_data           <- matrix(c(json_file, toString(name), "MULTIPLE END EMPTY", toString(query_name),       toString(query_class),             query_index,                      hit_index_min,                hit_value_min,             paste(hit_names_min, sep="", collapse=","),                                    paste(hit_index_min_values, sep="", collapse=","),             NA,        NA), nrow=1, ncol=len_col_names_debug_matrix_data, byrow=T)
            #                              "filename",    "col_name", "status",                     "query_name",               "query_class",            "query_index",                    "hit_index_min",              "hit_value_min",                 "hit_name_min",                                                                "hit_index_min_values",                      "hit_class_min", "res"
            debug_matrix_data <<- rbind(debug_matrix_data, row_data)
            
            next()
          }


          found <- polytomy_handler( mult_found )


          if ( ! found ) {
            print("NOT FOUND")
  
            if ( all( sapply(mult_found, is.na) )) {
              print("ALL ARE NA")
              print(sapply(mult_found, is.na))
              print(paste("  MULTIPLE END file", json_file, "name",                 name,"x",x,"query_name",        query_name, "query_class",  query_class,"query_index",query_index,"h",h,"hit_index_min",hit_index_min,"hit_value_min",hit_value_min,"h_name_min",paste(hit_names_min, sep="", collapse=","),"hit_index_min_values",paste(hit_index_min_values, sep="", collapse=","), "res",          NA))
              row_data           <- matrix(c(json_file, toString(name), "MULTIPLE END NA", toString(query_name),       toString(query_class),             query_index,                      hit_index_min,                hit_value_min,             paste(hit_names_min, sep="", collapse=","),                       paste(hit_index_min_values, sep="", collapse=","), NA,             NA), nrow=1, ncol=len_col_names_debug_matrix_data, byrow=T)
              #                              "filename",    "col_name", "status",               "query_name",               "query_class",            "query_index",                    "hit_index_min",              "hit_value_min",                 "hit_name_min",                                                   "hit_index_min_values",                      "hit_class_min", "res"
              debug_matrix_data <<- rbind(debug_matrix_data, row_data)
              next()

            } else {
              print("REAL FALSE")
            }
          }
          
          print(paste("  MULTIPLE END file", json_file, "name",                 name,"x",x,"query_name",        query_name, "query_class",  query_class,"query_index",query_index,"h",h,"hit_index_min",hit_index_min,"hit_value_min",hit_value_min,"h_name_min",paste(hit_names_min, sep="", collapse=","),"hit_index_min_values",paste(hit_index_min_values, sep="", collapse=","), "res",          found))
          row_data           <- matrix(c(json_file, toString(name), "MULTIPLE END", toString(query_name),       toString(query_class),             query_index,                      hit_index_min,                hit_value_min,             paste(hit_names_min, sep="", collapse=","),                       paste(hit_index_min_values, sep="", collapse=","), NA,             found), nrow=1, ncol=len_col_names_debug_matrix_data, byrow=T)
          #                              "filename",    "col_name", "status",               "query_name",               "query_class",            "query_index",                    "hit_index_min",              "hit_value_min",                 "hit_name_min",                                                   "hit_index_min_values",                      "hit_class_min", "res"
          debug_matrix_data <<- rbind(debug_matrix_data, row_data)
          
          return( found )

        } else {
          if ( query_index == hit_index_min ) {
            next()
          }
          
          if ( ! (hit_names_min[1] %in% data_names ) ) {
            next()
          }
          
          hit_class_min_i <- which(data_names==hit_names_min[1], arr.ind=T)
          hit_class_min_n <- data_names[  hit_class_min_i]
          hit_class_min_v <- data_classes[hit_class_min_i]

          res           <- (query_class == hit_class_min_v)
#           print(paste("  SINGLE       file", json_file, "name",                 name, "x", x, "query_name", query_name, "query_class", query_class,"query_index",query_index, "hit_index_min",hit_index_min,"hit_value_min",hit_value_min,"h_name_min",paste(hit_names_min, sep="", collapse=","),"hit_index_min_values",paste(hit_index_min_values, sep="", collapse=","),"hit_class_min",toString(hit_class_min_v),"res", res))
          row_data           <- matrix(c(    json_file,                toString(name), "SINGLE",   toString(query_name),      toString(query_class),             query_index,                 hit_index_min,                hit_value_min,             paste(hit_names_min, sep="", collapse=","),                       paste(hit_index_min_values, sep="", collapse=","),                toString(hit_class_min_v),       res), nrow=1, ncol=len_col_names_debug_matrix_data, byrow=T)
          #                                 "filename",                    "col_name", "status",           "query_name",              "query_class",            "query_index",               "hit_index_min",              "hit_value_min",                  "hit_name_min",                                                  "hit_index_min_values",                                              "hit_class_min"  ,      "res"

          if (F) {
            print("hit_index_min"  )
            print(hit_index_min    )
            print("hit_names_min"  )
            print(hit_names_min[1] )
            print("hit_class_min_i")
            print(hit_class_min_i  )
            print("hit_class_min_n")
            print(hit_class_min_n  )
            print("hit_class_min_v")
            print(hit_class_min_v  )
            print("res")
            print(res)
          }

          debug_matrix_data <<- rbind(debug_matrix_data, row_data)
          return( res )
        }
      }
    } else {
      return(NA)
#       print(paste("spp", query_name, "not in matrix"))
#       stop()
    }
  }






  gen_filter_l <- function(name, class_data) { function(x) { filter_l(name, class_data, x) } }


#   print(debug_matrix_data)
  valid_cols             <- {}
  valid_cols.names       <- c()
  valid_cols.means       <- c()
  valid_cols.num_classes <- c()
  valid_cols.num_samples <- c()

  for ( col_name in classes_data_col_names ) {
    print(paste("analysing ", col_name))
    col_data  <- classes_data[ c(1,which(colnames(classes_data) == col_name, arr.ind=T)) ]
    col_data  <- col_data[col_data[col_name] != "", ]
    col_table <- table(col_data[col_name], exclude=c(NA, "", NULL))

    print(paste(" original diversity for",col_name,":",length(col_table)))
    if ( length(names(col_table)) == 1 ) {
      print(" no diversity here")
      next
    }
    print(col_table)

    col_table_single       <- col_table[col_table <= 1]
    col_table_single_names <- names(col_table_single)
    print(paste("col_table_single_names",col_table_single_names))



    if (length(col_table_single_names) > 0 ) {
      print(paste("  exluding", col_table_single_names))
      rows_to_del <- which(col_data[,2] %in% col_table_single_names, arr.ind=T)
      print(paste("   rows_to_del",rows_to_del))
      if (length(rows_to_del) > 0) {
        col_data <- col_data[-rows_to_del,]
      } else {
        print("     nothing to del")
      }
    }


    col_table <- table(col_data[col_name], exclude=c(NA, "", NULL))
#     print(paste("col_table names", names(col_table)))
#     col_table <- col_table[names(col_table) != ""]
#     print(col_table)
    col_table <- col_table[      col_table   > 1 ]
#     print(col_table)
    print(paste(" keeping:", names(col_table)))
    print(col_table)


    if ( length(col_table[col_table>1]) <= 1 ) {
      print(paste(" no diversity for",col_name,"after cleaning",length(col_table[col_table>1])))
      next()

    } else {
      print(paste(" diversity enought for",col_name,"after cleaning:", length(col_table[col_table>1])))

    }


    ind_col_data  <- unlist(lapply( 1:length(col_data[,1]), gen_filter_l(col_name, col_data) ))
    mean_col_data <- mean(ind_col_data, na.rm=T)

    if ( is.na(mean_col_data) ) {
      mean_col_data <- 0
    }

    print( paste(" % correctness", mean_col_data) )

    
#     print("debug_matrix_data END ROW")
#     print( debug_matrix_data         )  
#     stop()
    
    valid_cols.names       <- c(valid_cols.names      , col_name            )
    valid_cols.means       <- c(valid_cols.means      , mean_col_data       )
    valid_cols.num_classes <- c(valid_cols.num_classes, length(col_table   ))
    valid_cols.num_samples <- c(valid_cols.num_samples, length(col_data[,1]))
  }

#   print("debug_matrix_data END")
#   print( debug_matrix_data     )  
#   stop()

#   print(valid_cols.names       )
#   print(valid_cols.means       )
#   print(valid_cols.num_classes )
#   print(valid_cols.num_samples )
#   stop()
  
  res           <- matrix(c(valid_cols.num_classes, valid_cols.num_samples, valid_cols.means), nrow=3, ncol=length(valid_cols.names), byrow=T)
  colnames(res) <- valid_cols.names
  rownames(res) <- paste(json_file, "|", c("Number of Classes", "Number of Samples", "% of Correct Matches"))
  print(res)

  return(list("res"=res,"debug"=debug_matrix_data))
}