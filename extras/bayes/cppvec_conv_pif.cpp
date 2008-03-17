#include "conv_pif.hpp"

////////////// CONVERT C++ VECTOR TO AND FROM PYTHON LIST ///////////////////////////////

// Convert (C++) vector to (Python) list as PyObject*.
template<typename T> PyObject* cppvec2pylst(const vector<T>& vec)
{
  unsigned int i;
  boost::python::list lst;
  for(i=0; i<vec.size(); i++)
    lst.append(vec[i]);
  return boost::python::incref(boost::python::object(lst).ptr());
}

// Convert (Python) list to (C++) vector.
template<typename T> vector<T> pylst2cppvec(PyObject* obj)
{
  unsigned int i;
  vector<T> vec;
  boost::python::list lst(boost::python::borrowed(obj));
  unsigned int lstlen = extract<int>(lst.attr("__len__")());
  for(i=0; i<lstlen; i++)
    {
      T lstelem = extract<T>(lst[i]);
      vec.push_back(lstelem);
    }  
  return vec;
}

template<typename T>
struct cppvec_to_python_list
  {
    static PyObject* convert(const vector<T>& vec)
    {
      return cppvec2pylst(vec);
    }
};

template<typename T>
struct cppvec_from_python_list
{
  cppvec_from_python_list()
  {
    boost::python::converter::registry::push_back(
						  &convertible,
						  &construct,
						  boost::python::type_id<vector<T> >());
  }
  
  static void* convertible(PyObject* obj_ptr)
  {
    return obj_ptr;
  }
  
  static void construct(
			PyObject* obj_ptr,
			boost::python::converter::rvalue_from_python_stage1_data* data)
  {
    void* storage = (
		     (boost::python::converter::rvalue_from_python_storage<vector<T> >*)
		     data)->storage.bytes;
    new (storage) vector<T>(pylst2cppvec<T>(obj_ptr));
    data->convertible = storage;
  }
};

void export_cppvec_conv()
{
  boost::python::to_python_converter<vector<double>, cppvec_to_python_list<double> >();
  cppvec_from_python_list<double>();

  boost::python::to_python_converter<vector<int>, cppvec_to_python_list<int> >();
  cppvec_from_python_list<int>();

  boost::python::to_python_converter<vector<string>, cppvec_to_python_list<string> >();
  cppvec_from_python_list<string>();

  boost::python::to_python_converter<vector<blitz::TinyVector<int, 2> >, 
    cppvec_to_python_list<blitz::TinyVector<int, 2> > >();
  cppvec_from_python_list<blitz::TinyVector<int, 2> >();

  boost::python::to_python_converter<vector<blitz::TinyVector<int, 3> >, 
    cppvec_to_python_list<blitz::TinyVector<int, 3> > >();
  cppvec_from_python_list<blitz::TinyVector<int, 3> >();

  boost::python::to_python_converter<vector<blitz::TinyVector<double, 2> >, 
    cppvec_to_python_list<blitz::TinyVector<double, 2> > >();
  cppvec_from_python_list<blitz::TinyVector<double, 2> >();

  boost::python::to_python_converter<vector<blitz::TinyVector<double, 3> >, 
    cppvec_to_python_list<blitz::TinyVector<double, 3> > >();
  cppvec_from_python_list<blitz::TinyVector<double, 3> >();

  boost::python::to_python_converter<vector<ublas::vector<int> >, 
    cppvec_to_python_list<ublas::vector<int> > >();
  cppvec_from_python_list<ublas::vector<int> >();

  boost::python::to_python_converter<vector<ublas::vector<double> >, 
    cppvec_to_python_list<ublas::vector<double> > >();
  cppvec_from_python_list<ublas::vector<double> >();

  boost::python::to_python_converter<vector<ublas::vector<ublas::vector<int> > >, 
    cppvec_to_python_list<ublas::vector<ublas::vector<int> > > >();
  cppvec_from_python_list<ublas::vector<ublas::vector<int> > >();

  boost::python::to_python_converter<vector<ublas::vector<ublas::vector<double> > >, 
    cppvec_to_python_list<ublas::vector<ublas::vector<double> > > >();
  cppvec_from_python_list<ublas::vector<ublas::vector<double> > >();

  boost::python::to_python_converter<vector<ublas::vector<ublas::matrix<int> > >, 
    cppvec_to_python_list<ublas::vector<ublas::matrix<int> > > >();
  cppvec_from_python_list<ublas::vector<ublas::matrix<int> > >();

  boost::python::to_python_converter<vector<ublas::vector<ublas::matrix<double> > >, 
    cppvec_to_python_list<ublas::vector<ublas::matrix<double> > > >();
  cppvec_from_python_list<ublas::vector<ublas::matrix<double> > >();

}
