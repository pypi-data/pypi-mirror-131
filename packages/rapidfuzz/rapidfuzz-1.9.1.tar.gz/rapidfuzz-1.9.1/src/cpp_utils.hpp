#pragma once
#include "cpp_common.hpp"
#include <rapidfuzz/utils.hpp>

namespace utils = rapidfuzz::utils;

PyObject* default_process_impl(PyObject* sentence) {
    RF_String c_sentence = convert_string(sentence);

    switch (c_sentence.kind) {
#if PY_VERSION_HEX > PYTHON_VERSION(3, 0, 0)
    case RF_UINT8:
    {
        auto proc_str = utils::default_process(
            rapidfuzz::basic_string_view<uint8_t>(static_cast<uint8_t*>(c_sentence.data), c_sentence.length));
        return PyUnicode_FromKindAndData(PyUnicode_1BYTE_KIND, proc_str.data(), (Py_ssize_t)proc_str.size());
    }
    case RF_UINT16:
    {
        auto proc_str = utils::default_process(
            rapidfuzz::basic_string_view<uint16_t>(static_cast<uint16_t*>(c_sentence.data), c_sentence.length));
        return PyUnicode_FromKindAndData(PyUnicode_2BYTE_KIND, proc_str.data(), (Py_ssize_t)proc_str.size());
    }
    case RF_UINT32:
    {
        auto proc_str = utils::default_process(
            rapidfuzz::basic_string_view<uint32_t>(static_cast<uint32_t*>(c_sentence.data), c_sentence.length));
        return PyUnicode_FromKindAndData(PyUnicode_4BYTE_KIND, proc_str.data(), (Py_ssize_t)proc_str.size());
    }
#else
    case RF_CHAR:
    {
        auto proc_str = utils::default_process(
            rapidfuzz::basic_string_view<char>(static_cast<char*>(c_sentence.data), c_sentence.length));
        return PyString_FromStringAndSize(proc_str.data(), (Py_ssize_t)proc_str.size());
    }
    case RF_UNICODE:
    {
        auto proc_str = utils::default_process(
            rapidfuzz::basic_string_view<Py_UNICODE>(static_cast<Py_UNICODE*>(c_sentence.data), c_sentence.length));
        return PyUnicode_FromUnicode(proc_str.data(), (Py_ssize_t)proc_str.size());
    }
#endif
    // ToDo: for now do not process these elements should be done in some way in the future
    default:
        return sentence;
    }
}

template <typename CharT>
RF_String default_process_func_impl(RF_String sentence) {
    CharT* str = static_cast<CharT*>(sentence.data);

    if (!sentence.dtor)
    {
      CharT* temp_str = (CharT*)malloc(sentence.length * sizeof(CharT));
      if (temp_str == NULL)
      {
          throw std::bad_alloc();
      }
      std::copy(str, str + sentence.length, temp_str);
      str = temp_str;
    }

    sentence.dtor = default_string_deinit;
    sentence.data = str;
    sentence.kind = sentence.kind;
    sentence.length = utils::default_process(str, sentence.length);

    return sentence;
}

RF_String default_process_func(RF_String sentence) {
    switch (sentence.kind) {
    # define X_ENUM(KIND, TYPE) case KIND: return default_process_func_impl<TYPE>(std::move(sentence));
    LIST_OF_CASES()
    default:
       throw std::logic_error("Reached end of control flow in default_process_func");
    # undef X_ENUM
    }
}
