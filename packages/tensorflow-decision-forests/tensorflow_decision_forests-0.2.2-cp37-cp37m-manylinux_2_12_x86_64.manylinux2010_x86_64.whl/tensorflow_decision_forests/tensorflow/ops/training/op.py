"""Python wrappers around TensorFlow ops.

This file is MACHINE GENERATED! Do not edit.
Original C++ source file: op_py_no_precompile.cc
"""

import collections

from tensorflow.python import pywrap_tfe as pywrap_tfe
from tensorflow.python.eager import context as _context
from tensorflow.python.eager import core as _core
from tensorflow.python.eager import execute as _execute
from tensorflow.python.framework import dtypes as _dtypes

from tensorflow.python.framework import op_def_registry as _op_def_registry
from tensorflow.python.framework import ops as _ops
from tensorflow.python.framework import op_def_library as _op_def_library
from tensorflow.python.util.deprecation import deprecated_endpoints
from tensorflow.python.util import dispatch as _dispatch
from tensorflow.python.util.tf_export import tf_export

from typing import TypeVar

@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_categorical_int_feature')
def simple_ml_categorical_int_feature(value, id, feature_name, name=None):
  r"""TODO: add doc.

  Args:
    value: A `Tensor` of type `int32`.
    id: A `string`.
    feature_name: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLCategoricalIntFeature", name, value, "id", id,
        "feature_name", feature_name)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_categorical_int_feature(
          (value, id, feature_name, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_categorical_int_feature_eager_fallback(
          value, id=id, feature_name=feature_name, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_categorical_int_feature, (), dict(value=value, id=id,
                                                        feature_name=feature_name,
                                                        name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_categorical_int_feature(
        (value, id, feature_name, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLCategoricalIntFeature", value=value, id=id,
                                         feature_name=feature_name, name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_categorical_int_feature, (), dict(value=value, id=id,
                                                      feature_name=feature_name,
                                                      name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLCategoricalIntFeature = tf_export("raw_ops.SimpleMLCategoricalIntFeature")(_ops.to_raw_op(simple_ml_categorical_int_feature))
_dispatcher_for_simple_ml_categorical_int_feature = simple_ml_categorical_int_feature._tf_type_based_dispatcher.Dispatch


def simple_ml_categorical_int_feature_eager_fallback(value, id, feature_name, name, ctx):
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  value = _ops.convert_to_tensor(value, _dtypes.int32)
  _inputs_flat = [value]
  _attrs = ("id", id, "feature_name", feature_name)
  _result = _execute.execute(b"SimpleMLCategoricalIntFeature", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_categorical_int_feature_on_file')
def simple_ml_categorical_int_feature_on_file(value, resource_id, feature_idx, feature_name, dataset_path, name=None):
  r"""TODO: add doc.

  Args:
    value: A `Tensor` of type `int32`.
    resource_id: A `string`.
    feature_idx: An `int`.
    feature_name: A `string`.
    dataset_path: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLCategoricalIntFeatureOnFile", name, value,
        "resource_id", resource_id, "feature_idx", feature_idx,
        "feature_name", feature_name, "dataset_path", dataset_path)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_categorical_int_feature_on_file(
          (value, resource_id, feature_idx, feature_name, dataset_path,
          name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_categorical_int_feature_on_file_eager_fallback(
          value, resource_id=resource_id, feature_idx=feature_idx,
          feature_name=feature_name, dataset_path=dataset_path, name=name,
          ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_categorical_int_feature_on_file, (), dict(value=value,
                                                                resource_id=resource_id,
                                                                feature_idx=feature_idx,
                                                                feature_name=feature_name,
                                                                dataset_path=dataset_path,
                                                                name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_categorical_int_feature_on_file(
        (value, resource_id, feature_idx, feature_name, dataset_path, name,),
        None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  resource_id = _execute.make_str(resource_id, "resource_id")
  feature_idx = _execute.make_int(feature_idx, "feature_idx")
  feature_name = _execute.make_str(feature_name, "feature_name")
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLCategoricalIntFeatureOnFile", value=value,
                                               resource_id=resource_id,
                                               feature_idx=feature_idx,
                                               feature_name=feature_name,
                                               dataset_path=dataset_path,
                                               name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_categorical_int_feature_on_file, (), dict(value=value,
                                                              resource_id=resource_id,
                                                              feature_idx=feature_idx,
                                                              feature_name=feature_name,
                                                              dataset_path=dataset_path,
                                                              name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLCategoricalIntFeatureOnFile = tf_export("raw_ops.SimpleMLCategoricalIntFeatureOnFile")(_ops.to_raw_op(simple_ml_categorical_int_feature_on_file))
_dispatcher_for_simple_ml_categorical_int_feature_on_file = simple_ml_categorical_int_feature_on_file._tf_type_based_dispatcher.Dispatch


def simple_ml_categorical_int_feature_on_file_eager_fallback(value, resource_id, feature_idx, feature_name, dataset_path, name, ctx):
  resource_id = _execute.make_str(resource_id, "resource_id")
  feature_idx = _execute.make_int(feature_idx, "feature_idx")
  feature_name = _execute.make_str(feature_name, "feature_name")
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  value = _ops.convert_to_tensor(value, _dtypes.int32)
  _inputs_flat = [value]
  _attrs = ("resource_id", resource_id, "feature_idx", feature_idx,
  "feature_name", feature_name, "dataset_path", dataset_path)
  _result = _execute.execute(b"SimpleMLCategoricalIntFeatureOnFile", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_categorical_set_int_feature')
def simple_ml_categorical_set_int_feature(values, row_splits, id, feature_name, name=None):
  r"""TODO: add doc.

  Args:
    values: A `Tensor` of type `int32`.
    row_splits: A `Tensor` of type `int64`.
    id: A `string`.
    feature_name: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLCategoricalSetIntFeature", name, values, row_splits,
        "id", id, "feature_name", feature_name)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_categorical_set_int_feature(
          (values, row_splits, id, feature_name, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_categorical_set_int_feature_eager_fallback(
          values, row_splits, id=id, feature_name=feature_name, name=name,
          ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_categorical_set_int_feature, (), dict(values=values,
                                                            row_splits=row_splits,
                                                            id=id,
                                                            feature_name=feature_name,
                                                            name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_categorical_set_int_feature(
        (values, row_splits, id, feature_name, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLCategoricalSetIntFeature", values=values,
                                            row_splits=row_splits, id=id,
                                            feature_name=feature_name,
                                            name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_categorical_set_int_feature, (), dict(values=values,
                                                          row_splits=row_splits,
                                                          id=id,
                                                          feature_name=feature_name,
                                                          name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLCategoricalSetIntFeature = tf_export("raw_ops.SimpleMLCategoricalSetIntFeature")(_ops.to_raw_op(simple_ml_categorical_set_int_feature))
_dispatcher_for_simple_ml_categorical_set_int_feature = simple_ml_categorical_set_int_feature._tf_type_based_dispatcher.Dispatch


def simple_ml_categorical_set_int_feature_eager_fallback(values, row_splits, id, feature_name, name, ctx):
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  values = _ops.convert_to_tensor(values, _dtypes.int32)
  row_splits = _ops.convert_to_tensor(row_splits, _dtypes.int64)
  _inputs_flat = [values, row_splits]
  _attrs = ("id", id, "feature_name", feature_name)
  _result = _execute.execute(b"SimpleMLCategoricalSetIntFeature", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_categorical_set_string_feature')
def simple_ml_categorical_set_string_feature(values, row_splits, id, feature_name, name=None):
  r"""TODO: add doc.

  Args:
    values: A `Tensor` of type `string`.
    row_splits: A `Tensor` of type `int64`.
    id: A `string`.
    feature_name: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLCategoricalSetStringFeature", name, values, row_splits,
        "id", id, "feature_name", feature_name)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_categorical_set_string_feature(
          (values, row_splits, id, feature_name, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_categorical_set_string_feature_eager_fallback(
          values, row_splits, id=id, feature_name=feature_name, name=name,
          ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_categorical_set_string_feature, (), dict(values=values,
                                                               row_splits=row_splits,
                                                               id=id,
                                                               feature_name=feature_name,
                                                               name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_categorical_set_string_feature(
        (values, row_splits, id, feature_name, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLCategoricalSetStringFeature", values=values,
                                               row_splits=row_splits, id=id,
                                               feature_name=feature_name,
                                               name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_categorical_set_string_feature, (), dict(values=values,
                                                             row_splits=row_splits,
                                                             id=id,
                                                             feature_name=feature_name,
                                                             name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLCategoricalSetStringFeature = tf_export("raw_ops.SimpleMLCategoricalSetStringFeature")(_ops.to_raw_op(simple_ml_categorical_set_string_feature))
_dispatcher_for_simple_ml_categorical_set_string_feature = simple_ml_categorical_set_string_feature._tf_type_based_dispatcher.Dispatch


def simple_ml_categorical_set_string_feature_eager_fallback(values, row_splits, id, feature_name, name, ctx):
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  values = _ops.convert_to_tensor(values, _dtypes.string)
  row_splits = _ops.convert_to_tensor(row_splits, _dtypes.int64)
  _inputs_flat = [values, row_splits]
  _attrs = ("id", id, "feature_name", feature_name)
  _result = _execute.execute(b"SimpleMLCategoricalSetStringFeature", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_categorical_string_feature')
def simple_ml_categorical_string_feature(value, id, feature_name, name=None):
  r"""TODO: add doc.

  Args:
    value: A `Tensor` of type `string`.
    id: A `string`.
    feature_name: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLCategoricalStringFeature", name, value, "id", id,
        "feature_name", feature_name)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_categorical_string_feature(
          (value, id, feature_name, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_categorical_string_feature_eager_fallback(
          value, id=id, feature_name=feature_name, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_categorical_string_feature, (), dict(value=value, id=id,
                                                           feature_name=feature_name,
                                                           name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_categorical_string_feature(
        (value, id, feature_name, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLCategoricalStringFeature", value=value, id=id,
                                            feature_name=feature_name,
                                            name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_categorical_string_feature, (), dict(value=value, id=id,
                                                         feature_name=feature_name,
                                                         name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLCategoricalStringFeature = tf_export("raw_ops.SimpleMLCategoricalStringFeature")(_ops.to_raw_op(simple_ml_categorical_string_feature))
_dispatcher_for_simple_ml_categorical_string_feature = simple_ml_categorical_string_feature._tf_type_based_dispatcher.Dispatch


def simple_ml_categorical_string_feature_eager_fallback(value, id, feature_name, name, ctx):
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  value = _ops.convert_to_tensor(value, _dtypes.string)
  _inputs_flat = [value]
  _attrs = ("id", id, "feature_name", feature_name)
  _result = _execute.execute(b"SimpleMLCategoricalStringFeature", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_categorical_string_feature_on_file')
def simple_ml_categorical_string_feature_on_file(value, resource_id, feature_idx, feature_name, dataset_path, name=None):
  r"""TODO: add doc.

  Args:
    value: A `Tensor` of type `string`.
    resource_id: A `string`.
    feature_idx: An `int`.
    feature_name: A `string`.
    dataset_path: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLCategoricalStringFeatureOnFile", name, value,
        "resource_id", resource_id, "feature_idx", feature_idx,
        "feature_name", feature_name, "dataset_path", dataset_path)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_categorical_string_feature_on_file(
          (value, resource_id, feature_idx, feature_name, dataset_path,
          name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_categorical_string_feature_on_file_eager_fallback(
          value, resource_id=resource_id, feature_idx=feature_idx,
          feature_name=feature_name, dataset_path=dataset_path, name=name,
          ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_categorical_string_feature_on_file, (), dict(value=value,
                                                                   resource_id=resource_id,
                                                                   feature_idx=feature_idx,
                                                                   feature_name=feature_name,
                                                                   dataset_path=dataset_path,
                                                                   name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_categorical_string_feature_on_file(
        (value, resource_id, feature_idx, feature_name, dataset_path, name,),
        None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  resource_id = _execute.make_str(resource_id, "resource_id")
  feature_idx = _execute.make_int(feature_idx, "feature_idx")
  feature_name = _execute.make_str(feature_name, "feature_name")
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLCategoricalStringFeatureOnFile", value=value,
                                                  resource_id=resource_id,
                                                  feature_idx=feature_idx,
                                                  feature_name=feature_name,
                                                  dataset_path=dataset_path,
                                                  name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_categorical_string_feature_on_file, (), dict(value=value,
                                                                 resource_id=resource_id,
                                                                 feature_idx=feature_idx,
                                                                 feature_name=feature_name,
                                                                 dataset_path=dataset_path,
                                                                 name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLCategoricalStringFeatureOnFile = tf_export("raw_ops.SimpleMLCategoricalStringFeatureOnFile")(_ops.to_raw_op(simple_ml_categorical_string_feature_on_file))
_dispatcher_for_simple_ml_categorical_string_feature_on_file = simple_ml_categorical_string_feature_on_file._tf_type_based_dispatcher.Dispatch


def simple_ml_categorical_string_feature_on_file_eager_fallback(value, resource_id, feature_idx, feature_name, dataset_path, name, ctx):
  resource_id = _execute.make_str(resource_id, "resource_id")
  feature_idx = _execute.make_int(feature_idx, "feature_idx")
  feature_name = _execute.make_str(feature_name, "feature_name")
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  value = _ops.convert_to_tensor(value, _dtypes.string)
  _inputs_flat = [value]
  _attrs = ("resource_id", resource_id, "feature_idx", feature_idx,
  "feature_name", feature_name, "dataset_path", dataset_path)
  _result = _execute.execute(b"SimpleMLCategoricalStringFeatureOnFile", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_chief_finalize_feature_on_file')
def simple_ml_chief_finalize_feature_on_file(feature_names, dataset_path, num_shards, name=None):
  r"""TODO: add doc.

  Args:
    feature_names: A list of `strings`.
    dataset_path: A `string`.
    num_shards: An `int`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLChiefFinalizeFeatureOnFile", name, "feature_names",
        feature_names, "dataset_path", dataset_path, "num_shards", num_shards)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_chief_finalize_feature_on_file(
          (feature_names, dataset_path, num_shards, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_chief_finalize_feature_on_file_eager_fallback(
          feature_names=feature_names, dataset_path=dataset_path,
          num_shards=num_shards, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_chief_finalize_feature_on_file, (), dict(feature_names=feature_names,
                                                               dataset_path=dataset_path,
                                                               num_shards=num_shards,
                                                               name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_chief_finalize_feature_on_file(
        (feature_names, dataset_path, num_shards, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  if not isinstance(feature_names, (list, tuple)):
    raise TypeError(
        "Expected list for 'feature_names' argument to "
        "'simple_ml_chief_finalize_feature_on_file' Op, not %r." % feature_names)
  feature_names = [_execute.make_str(_s, "feature_names") for _s in feature_names]
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  num_shards = _execute.make_int(num_shards, "num_shards")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLChiefFinalizeFeatureOnFile", feature_names=feature_names,
                                              dataset_path=dataset_path,
                                              num_shards=num_shards,
                                              name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_chief_finalize_feature_on_file, (), dict(feature_names=feature_names,
                                                             dataset_path=dataset_path,
                                                             num_shards=num_shards,
                                                             name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLChiefFinalizeFeatureOnFile = tf_export("raw_ops.SimpleMLChiefFinalizeFeatureOnFile")(_ops.to_raw_op(simple_ml_chief_finalize_feature_on_file))
_dispatcher_for_simple_ml_chief_finalize_feature_on_file = simple_ml_chief_finalize_feature_on_file._tf_type_based_dispatcher.Dispatch


def simple_ml_chief_finalize_feature_on_file_eager_fallback(feature_names, dataset_path, num_shards, name, ctx):
  if not isinstance(feature_names, (list, tuple)):
    raise TypeError(
        "Expected list for 'feature_names' argument to "
        "'simple_ml_chief_finalize_feature_on_file' Op, not %r." % feature_names)
  feature_names = [_execute.make_str(_s, "feature_names") for _s in feature_names]
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  num_shards = _execute.make_int(num_shards, "num_shards")
  _inputs_flat = []
  _attrs = ("feature_names", feature_names, "dataset_path", dataset_path,
  "num_shards", num_shards)
  _result = _execute.execute(b"SimpleMLChiefFinalizeFeatureOnFile", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_file_model_loader')
def simple_ml_file_model_loader(model_path, model_identifier, name=None):
  r"""TODO: add doc.

  Args:
    model_path: A `Tensor` of type `string`.
    model_identifier: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLFileModelLoader", name, model_path, "model_identifier",
        model_identifier)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_file_model_loader(
          (model_path, model_identifier, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_file_model_loader_eager_fallback(
          model_path, model_identifier=model_identifier, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_file_model_loader, (), dict(model_path=model_path,
                                                  model_identifier=model_identifier,
                                                  name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_file_model_loader(
        (model_path, model_identifier, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  model_identifier = _execute.make_str(model_identifier, "model_identifier")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLFileModelLoader", model_path=model_path,
                                   model_identifier=model_identifier,
                                   name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_file_model_loader, (), dict(model_path=model_path,
                                                model_identifier=model_identifier,
                                                name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLFileModelLoader = tf_export("raw_ops.SimpleMLFileModelLoader")(_ops.to_raw_op(simple_ml_file_model_loader))
_dispatcher_for_simple_ml_file_model_loader = simple_ml_file_model_loader._tf_type_based_dispatcher.Dispatch


def simple_ml_file_model_loader_eager_fallback(model_path, model_identifier, name, ctx):
  model_identifier = _execute.make_str(model_identifier, "model_identifier")
  model_path = _ops.convert_to_tensor(model_path, _dtypes.string)
  _inputs_flat = [model_path]
  _attrs = ("model_identifier", model_identifier)
  _result = _execute.execute(b"SimpleMLFileModelLoader", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_hash_feature')
def simple_ml_hash_feature(value, id, feature_name, name=None):
  r"""TODO: add doc.

  Args:
    value: A `Tensor` of type `string`.
    id: A `string`.
    feature_name: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLHashFeature", name, value, "id", id, "feature_name",
        feature_name)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_hash_feature(
          (value, id, feature_name, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_hash_feature_eager_fallback(
          value, id=id, feature_name=feature_name, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_hash_feature, (), dict(value=value, id=id,
                                             feature_name=feature_name,
                                             name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_hash_feature(
        (value, id, feature_name, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLHashFeature", value=value, id=id, feature_name=feature_name,
                               name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_hash_feature, (), dict(value=value, id=id,
                                           feature_name=feature_name,
                                           name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLHashFeature = tf_export("raw_ops.SimpleMLHashFeature")(_ops.to_raw_op(simple_ml_hash_feature))
_dispatcher_for_simple_ml_hash_feature = simple_ml_hash_feature._tf_type_based_dispatcher.Dispatch


def simple_ml_hash_feature_eager_fallback(value, id, feature_name, name, ctx):
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  value = _ops.convert_to_tensor(value, _dtypes.string)
  _inputs_flat = [value]
  _attrs = ("id", id, "feature_name", feature_name)
  _result = _execute.execute(b"SimpleMLHashFeature", 0, inputs=_inputs_flat,
                             attrs=_attrs, ctx=ctx, name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_model_trainer')
def simple_ml_model_trainer(feature_ids, label_id, weight_id, model_id, model_dir, learner, hparams, task, training_config, deployment_config, guide="", has_validation_dataset=False, name=None):
  r"""TODO: add doc.

  Args:
    feature_ids: A `string`.
    label_id: A `string`.
    weight_id: A `string`.
    model_id: A `string`.
    model_dir: A `string`.
    learner: A `string`.
    hparams: A `string`.
    task: An `int`.
    training_config: A `string`.
    deployment_config: A `string`.
    guide: An optional `string`. Defaults to `""`.
    has_validation_dataset: An optional `bool`. Defaults to `False`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `bool`.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLModelTrainer", name, "feature_ids", feature_ids,
        "label_id", label_id, "weight_id", weight_id, "model_id", model_id,
        "model_dir", model_dir, "learner", learner, "hparams", hparams,
        "task", task, "training_config", training_config, "deployment_config",
        deployment_config, "guide", guide, "has_validation_dataset",
        has_validation_dataset)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_model_trainer(
          (feature_ids, label_id, weight_id, model_id, model_dir, learner,
          hparams, task, training_config, deployment_config, guide,
          has_validation_dataset, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_model_trainer_eager_fallback(
          feature_ids=feature_ids, label_id=label_id, weight_id=weight_id,
          model_id=model_id, model_dir=model_dir, learner=learner,
          hparams=hparams, task=task, training_config=training_config,
          deployment_config=deployment_config, guide=guide,
          has_validation_dataset=has_validation_dataset, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_model_trainer, (), dict(feature_ids=feature_ids,
                                              label_id=label_id,
                                              weight_id=weight_id,
                                              model_id=model_id,
                                              model_dir=model_dir,
                                              learner=learner,
                                              hparams=hparams, task=task,
                                              training_config=training_config,
                                              deployment_config=deployment_config,
                                              guide=guide,
                                              has_validation_dataset=has_validation_dataset,
                                              name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_model_trainer(
        (feature_ids, label_id, weight_id, model_id, model_dir, learner,
        hparams, task, training_config, deployment_config, guide,
        has_validation_dataset, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  feature_ids = _execute.make_str(feature_ids, "feature_ids")
  label_id = _execute.make_str(label_id, "label_id")
  weight_id = _execute.make_str(weight_id, "weight_id")
  model_id = _execute.make_str(model_id, "model_id")
  model_dir = _execute.make_str(model_dir, "model_dir")
  learner = _execute.make_str(learner, "learner")
  hparams = _execute.make_str(hparams, "hparams")
  task = _execute.make_int(task, "task")
  training_config = _execute.make_str(training_config, "training_config")
  deployment_config = _execute.make_str(deployment_config, "deployment_config")
  if guide is None:
    guide = ""
  guide = _execute.make_str(guide, "guide")
  if has_validation_dataset is None:
    has_validation_dataset = False
  has_validation_dataset = _execute.make_bool(has_validation_dataset, "has_validation_dataset")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLModelTrainer", feature_ids=feature_ids, label_id=label_id,
                                weight_id=weight_id, model_id=model_id,
                                model_dir=model_dir, learner=learner,
                                hparams=hparams, task=task,
                                training_config=training_config,
                                deployment_config=deployment_config,
                                guide=guide,
                                has_validation_dataset=has_validation_dataset,
                                name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_model_trainer, (), dict(feature_ids=feature_ids,
                                            label_id=label_id,
                                            weight_id=weight_id,
                                            model_id=model_id,
                                            model_dir=model_dir,
                                            learner=learner, hparams=hparams,
                                            task=task,
                                            training_config=training_config,
                                            deployment_config=deployment_config,
                                            guide=guide,
                                            has_validation_dataset=has_validation_dataset,
                                            name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  _result = _outputs[:]
  if _execute.must_record_gradient():
    _attrs = ("feature_ids", _op.get_attr("feature_ids"), "label_id",
              _op.get_attr("label_id"), "weight_id",
              _op.get_attr("weight_id"), "model_id", _op.get_attr("model_id"),
              "model_dir", _op.get_attr("model_dir"), "learner",
              _op.get_attr("learner"), "hparams", _op.get_attr("hparams"),
              "task", _op._get_attr_int("task"), "training_config",
              _op.get_attr("training_config"), "deployment_config",
              _op.get_attr("deployment_config"), "guide",
              _op.get_attr("guide"), "has_validation_dataset",
              _op._get_attr_bool("has_validation_dataset"))
    _inputs_flat = _op.inputs
    _execute.record_gradient(
        "SimpleMLModelTrainer", _inputs_flat, _attrs, _result)
  _result, = _result
  return _result

SimpleMLModelTrainer = tf_export("raw_ops.SimpleMLModelTrainer")(_ops.to_raw_op(simple_ml_model_trainer))
_dispatcher_for_simple_ml_model_trainer = simple_ml_model_trainer._tf_type_based_dispatcher.Dispatch


def simple_ml_model_trainer_eager_fallback(feature_ids, label_id, weight_id, model_id, model_dir, learner, hparams, task, training_config, deployment_config, guide, has_validation_dataset, name, ctx):
  feature_ids = _execute.make_str(feature_ids, "feature_ids")
  label_id = _execute.make_str(label_id, "label_id")
  weight_id = _execute.make_str(weight_id, "weight_id")
  model_id = _execute.make_str(model_id, "model_id")
  model_dir = _execute.make_str(model_dir, "model_dir")
  learner = _execute.make_str(learner, "learner")
  hparams = _execute.make_str(hparams, "hparams")
  task = _execute.make_int(task, "task")
  training_config = _execute.make_str(training_config, "training_config")
  deployment_config = _execute.make_str(deployment_config, "deployment_config")
  if guide is None:
    guide = ""
  guide = _execute.make_str(guide, "guide")
  if has_validation_dataset is None:
    has_validation_dataset = False
  has_validation_dataset = _execute.make_bool(has_validation_dataset, "has_validation_dataset")
  _inputs_flat = []
  _attrs = ("feature_ids", feature_ids, "label_id", label_id, "weight_id",
  weight_id, "model_id", model_id, "model_dir", model_dir, "learner", learner,
  "hparams", hparams, "task", task, "training_config", training_config,
  "deployment_config", deployment_config, "guide", guide,
  "has_validation_dataset", has_validation_dataset)
  _result = _execute.execute(b"SimpleMLModelTrainer", 1, inputs=_inputs_flat,
                             attrs=_attrs, ctx=ctx, name=name)
  if _execute.must_record_gradient():
    _execute.record_gradient(
        "SimpleMLModelTrainer", _inputs_flat, _attrs, _result)
  _result, = _result
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_model_trainer_on_file')
def simple_ml_model_trainer_on_file(train_dataset_path, model_id, model_dir, hparams, training_config, deployment_config, valid_dataset_path="", guide="", name=None):
  r"""TODO: add doc.

  Args:
    train_dataset_path: A `string`.
    model_id: A `string`.
    model_dir: A `string`.
    hparams: A `string`.
    training_config: A `string`.
    deployment_config: A `string`.
    valid_dataset_path: An optional `string`. Defaults to `""`.
    guide: An optional `string`. Defaults to `""`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `bool`.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLModelTrainerOnFile", name, "train_dataset_path",
        train_dataset_path, "valid_dataset_path", valid_dataset_path,
        "model_id", model_id, "model_dir", model_dir, "hparams", hparams,
        "training_config", training_config, "deployment_config",
        deployment_config, "guide", guide)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_model_trainer_on_file(
          (train_dataset_path, model_id, model_dir, hparams, training_config,
          deployment_config, valid_dataset_path, guide, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_model_trainer_on_file_eager_fallback(
          train_dataset_path=train_dataset_path,
          valid_dataset_path=valid_dataset_path, model_id=model_id,
          model_dir=model_dir, hparams=hparams,
          training_config=training_config,
          deployment_config=deployment_config, guide=guide, name=name,
          ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_model_trainer_on_file, (), dict(train_dataset_path=train_dataset_path,
                                                      model_id=model_id,
                                                      model_dir=model_dir,
                                                      hparams=hparams,
                                                      training_config=training_config,
                                                      deployment_config=deployment_config,
                                                      valid_dataset_path=valid_dataset_path,
                                                      guide=guide, name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_model_trainer_on_file(
        (train_dataset_path, model_id, model_dir, hparams, training_config,
        deployment_config, valid_dataset_path, guide, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  train_dataset_path = _execute.make_str(train_dataset_path, "train_dataset_path")
  model_id = _execute.make_str(model_id, "model_id")
  model_dir = _execute.make_str(model_dir, "model_dir")
  hparams = _execute.make_str(hparams, "hparams")
  training_config = _execute.make_str(training_config, "training_config")
  deployment_config = _execute.make_str(deployment_config, "deployment_config")
  if valid_dataset_path is None:
    valid_dataset_path = ""
  valid_dataset_path = _execute.make_str(valid_dataset_path, "valid_dataset_path")
  if guide is None:
    guide = ""
  guide = _execute.make_str(guide, "guide")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLModelTrainerOnFile", train_dataset_path=train_dataset_path,
                                      model_id=model_id, model_dir=model_dir,
                                      hparams=hparams,
                                      training_config=training_config,
                                      deployment_config=deployment_config,
                                      valid_dataset_path=valid_dataset_path,
                                      guide=guide, name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_model_trainer_on_file, (), dict(train_dataset_path=train_dataset_path,
                                                    model_id=model_id,
                                                    model_dir=model_dir,
                                                    hparams=hparams,
                                                    training_config=training_config,
                                                    deployment_config=deployment_config,
                                                    valid_dataset_path=valid_dataset_path,
                                                    guide=guide, name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  _result = _outputs[:]
  if _execute.must_record_gradient():
    _attrs = ("train_dataset_path", _op.get_attr("train_dataset_path"),
              "valid_dataset_path", _op.get_attr("valid_dataset_path"),
              "model_id", _op.get_attr("model_id"), "model_dir",
              _op.get_attr("model_dir"), "hparams", _op.get_attr("hparams"),
              "training_config", _op.get_attr("training_config"),
              "deployment_config", _op.get_attr("deployment_config"), "guide",
              _op.get_attr("guide"))
    _inputs_flat = _op.inputs
    _execute.record_gradient(
        "SimpleMLModelTrainerOnFile", _inputs_flat, _attrs, _result)
  _result, = _result
  return _result

SimpleMLModelTrainerOnFile = tf_export("raw_ops.SimpleMLModelTrainerOnFile")(_ops.to_raw_op(simple_ml_model_trainer_on_file))
_dispatcher_for_simple_ml_model_trainer_on_file = simple_ml_model_trainer_on_file._tf_type_based_dispatcher.Dispatch


def simple_ml_model_trainer_on_file_eager_fallback(train_dataset_path, model_id, model_dir, hparams, training_config, deployment_config, valid_dataset_path, guide, name, ctx):
  train_dataset_path = _execute.make_str(train_dataset_path, "train_dataset_path")
  model_id = _execute.make_str(model_id, "model_id")
  model_dir = _execute.make_str(model_dir, "model_dir")
  hparams = _execute.make_str(hparams, "hparams")
  training_config = _execute.make_str(training_config, "training_config")
  deployment_config = _execute.make_str(deployment_config, "deployment_config")
  if valid_dataset_path is None:
    valid_dataset_path = ""
  valid_dataset_path = _execute.make_str(valid_dataset_path, "valid_dataset_path")
  if guide is None:
    guide = ""
  guide = _execute.make_str(guide, "guide")
  _inputs_flat = []
  _attrs = ("train_dataset_path", train_dataset_path, "valid_dataset_path",
  valid_dataset_path, "model_id", model_id, "model_dir", model_dir, "hparams",
  hparams, "training_config", training_config, "deployment_config",
  deployment_config, "guide", guide)
  _result = _execute.execute(b"SimpleMLModelTrainerOnFile", 1,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  if _execute.must_record_gradient():
    _execute.record_gradient(
        "SimpleMLModelTrainerOnFile", _inputs_flat, _attrs, _result)
  _result, = _result
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_numerical_feature')
def simple_ml_numerical_feature(value, id, feature_name, name=None):
  r"""TODO: add doc.

  Args:
    value: A `Tensor` of type `float32`.
    id: A `string`.
    feature_name: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLNumericalFeature", name, value, "id", id,
        "feature_name", feature_name)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_numerical_feature(
          (value, id, feature_name, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_numerical_feature_eager_fallback(
          value, id=id, feature_name=feature_name, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_numerical_feature, (), dict(value=value, id=id,
                                                  feature_name=feature_name,
                                                  name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_numerical_feature(
        (value, id, feature_name, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLNumericalFeature", value=value, id=id,
                                    feature_name=feature_name, name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_numerical_feature, (), dict(value=value, id=id,
                                                feature_name=feature_name,
                                                name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLNumericalFeature = tf_export("raw_ops.SimpleMLNumericalFeature")(_ops.to_raw_op(simple_ml_numerical_feature))
_dispatcher_for_simple_ml_numerical_feature = simple_ml_numerical_feature._tf_type_based_dispatcher.Dispatch


def simple_ml_numerical_feature_eager_fallback(value, id, feature_name, name, ctx):
  id = _execute.make_str(id, "id")
  feature_name = _execute.make_str(feature_name, "feature_name")
  value = _ops.convert_to_tensor(value, _dtypes.float32)
  _inputs_flat = [value]
  _attrs = ("id", id, "feature_name", feature_name)
  _result = _execute.execute(b"SimpleMLNumericalFeature", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_numerical_feature_on_file')
def simple_ml_numerical_feature_on_file(value, resource_id, feature_idx, feature_name, dataset_path, name=None):
  r"""TODO: add doc.

  Args:
    value: A `Tensor` of type `float32`.
    resource_id: A `string`.
    feature_idx: An `int`.
    feature_name: A `string`.
    dataset_path: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLNumericalFeatureOnFile", name, value, "resource_id",
        resource_id, "feature_idx", feature_idx, "feature_name", feature_name,
        "dataset_path", dataset_path)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_numerical_feature_on_file(
          (value, resource_id, feature_idx, feature_name, dataset_path,
          name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_numerical_feature_on_file_eager_fallback(
          value, resource_id=resource_id, feature_idx=feature_idx,
          feature_name=feature_name, dataset_path=dataset_path, name=name,
          ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_numerical_feature_on_file, (), dict(value=value,
                                                          resource_id=resource_id,
                                                          feature_idx=feature_idx,
                                                          feature_name=feature_name,
                                                          dataset_path=dataset_path,
                                                          name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_numerical_feature_on_file(
        (value, resource_id, feature_idx, feature_name, dataset_path, name,),
        None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  resource_id = _execute.make_str(resource_id, "resource_id")
  feature_idx = _execute.make_int(feature_idx, "feature_idx")
  feature_name = _execute.make_str(feature_name, "feature_name")
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLNumericalFeatureOnFile", value=value,
                                          resource_id=resource_id,
                                          feature_idx=feature_idx,
                                          feature_name=feature_name,
                                          dataset_path=dataset_path,
                                          name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_numerical_feature_on_file, (), dict(value=value,
                                                        resource_id=resource_id,
                                                        feature_idx=feature_idx,
                                                        feature_name=feature_name,
                                                        dataset_path=dataset_path,
                                                        name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLNumericalFeatureOnFile = tf_export("raw_ops.SimpleMLNumericalFeatureOnFile")(_ops.to_raw_op(simple_ml_numerical_feature_on_file))
_dispatcher_for_simple_ml_numerical_feature_on_file = simple_ml_numerical_feature_on_file._tf_type_based_dispatcher.Dispatch


def simple_ml_numerical_feature_on_file_eager_fallback(value, resource_id, feature_idx, feature_name, dataset_path, name, ctx):
  resource_id = _execute.make_str(resource_id, "resource_id")
  feature_idx = _execute.make_int(feature_idx, "feature_idx")
  feature_name = _execute.make_str(feature_name, "feature_name")
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  value = _ops.convert_to_tensor(value, _dtypes.float32)
  _inputs_flat = [value]
  _attrs = ("resource_id", resource_id, "feature_idx", feature_idx,
  "feature_name", feature_name, "dataset_path", dataset_path)
  _result = _execute.execute(b"SimpleMLNumericalFeatureOnFile", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_show_model')
def simple_ml_show_model(model_identifier, name=None):
  r"""TODO: add doc.

  Args:
    model_identifier: A `string`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLShowModel", name, "model_identifier", model_identifier)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_show_model(
          (model_identifier, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_show_model_eager_fallback(
          model_identifier=model_identifier, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_show_model, (), dict(model_identifier=model_identifier,
                                           name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_show_model(
        (model_identifier, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  model_identifier = _execute.make_str(model_identifier, "model_identifier")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLShowModel", model_identifier=model_identifier, name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_show_model, (), dict(model_identifier=model_identifier,
                                         name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  _result = _outputs[:]
  if _execute.must_record_gradient():
    _attrs = ("model_identifier", _op.get_attr("model_identifier"))
    _inputs_flat = _op.inputs
    _execute.record_gradient(
        "SimpleMLShowModel", _inputs_flat, _attrs, _result)
  _result, = _result
  return _result

SimpleMLShowModel = tf_export("raw_ops.SimpleMLShowModel")(_ops.to_raw_op(simple_ml_show_model))
_dispatcher_for_simple_ml_show_model = simple_ml_show_model._tf_type_based_dispatcher.Dispatch


def simple_ml_show_model_eager_fallback(model_identifier, name, ctx):
  model_identifier = _execute.make_str(model_identifier, "model_identifier")
  _inputs_flat = []
  _attrs = ("model_identifier", model_identifier)
  _result = _execute.execute(b"SimpleMLShowModel", 1, inputs=_inputs_flat,
                             attrs=_attrs, ctx=ctx, name=name)
  if _execute.must_record_gradient():
    _execute.record_gradient(
        "SimpleMLShowModel", _inputs_flat, _attrs, _result)
  _result, = _result
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_unload_model')
def simple_ml_unload_model(model_identifier, name=None):
  r"""TODO: add doc.

  Args:
    model_identifier: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLUnloadModel", name, "model_identifier",
        model_identifier)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_unload_model(
          (model_identifier, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_unload_model_eager_fallback(
          model_identifier=model_identifier, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_unload_model, (), dict(model_identifier=model_identifier,
                                             name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_unload_model(
        (model_identifier, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  model_identifier = _execute.make_str(model_identifier, "model_identifier")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLUnloadModel", model_identifier=model_identifier, name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_unload_model, (), dict(model_identifier=model_identifier,
                                           name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLUnloadModel = tf_export("raw_ops.SimpleMLUnloadModel")(_ops.to_raw_op(simple_ml_unload_model))
_dispatcher_for_simple_ml_unload_model = simple_ml_unload_model._tf_type_based_dispatcher.Dispatch


def simple_ml_unload_model_eager_fallback(model_identifier, name, ctx):
  model_identifier = _execute.make_str(model_identifier, "model_identifier")
  _inputs_flat = []
  _attrs = ("model_identifier", model_identifier)
  _result = _execute.execute(b"SimpleMLUnloadModel", 0, inputs=_inputs_flat,
                             attrs=_attrs, ctx=ctx, name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('simple_ml_worker_finalize_feature_on_file')
def simple_ml_worker_finalize_feature_on_file(feature_resource_ids, dataset_path, name=None):
  r"""TODO: add doc.

  Args:
    feature_resource_ids: A list of `strings`.
    dataset_path: A `string`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "SimpleMLWorkerFinalizeFeatureOnFile", name,
        "feature_resource_ids", feature_resource_ids, "dataset_path",
        dataset_path)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_simple_ml_worker_finalize_feature_on_file(
          (feature_resource_ids, dataset_path, name,), None)
      if _result is not NotImplemented:
        return _result
      return simple_ml_worker_finalize_feature_on_file_eager_fallback(
          feature_resource_ids=feature_resource_ids,
          dataset_path=dataset_path, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            simple_ml_worker_finalize_feature_on_file, (), dict(feature_resource_ids=feature_resource_ids,
                                                                dataset_path=dataset_path,
                                                                name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_simple_ml_worker_finalize_feature_on_file(
        (feature_resource_ids, dataset_path, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  if not isinstance(feature_resource_ids, (list, tuple)):
    raise TypeError(
        "Expected list for 'feature_resource_ids' argument to "
        "'simple_ml_worker_finalize_feature_on_file' Op, not %r." % feature_resource_ids)
  feature_resource_ids = [_execute.make_str(_s, "feature_resource_ids") for _s in feature_resource_ids]
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "SimpleMLWorkerFinalizeFeatureOnFile", feature_resource_ids=feature_resource_ids,
                                               dataset_path=dataset_path,
                                               name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          simple_ml_worker_finalize_feature_on_file, (), dict(feature_resource_ids=feature_resource_ids,
                                                              dataset_path=dataset_path,
                                                              name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
SimpleMLWorkerFinalizeFeatureOnFile = tf_export("raw_ops.SimpleMLWorkerFinalizeFeatureOnFile")(_ops.to_raw_op(simple_ml_worker_finalize_feature_on_file))
_dispatcher_for_simple_ml_worker_finalize_feature_on_file = simple_ml_worker_finalize_feature_on_file._tf_type_based_dispatcher.Dispatch


def simple_ml_worker_finalize_feature_on_file_eager_fallback(feature_resource_ids, dataset_path, name, ctx):
  if not isinstance(feature_resource_ids, (list, tuple)):
    raise TypeError(
        "Expected list for 'feature_resource_ids' argument to "
        "'simple_ml_worker_finalize_feature_on_file' Op, not %r." % feature_resource_ids)
  feature_resource_ids = [_execute.make_str(_s, "feature_resource_ids") for _s in feature_resource_ids]
  dataset_path = _execute.make_str(dataset_path, "dataset_path")
  _inputs_flat = []
  _attrs = ("feature_resource_ids", feature_resource_ids, "dataset_path",
  dataset_path)
  _result = _execute.execute(b"SimpleMLWorkerFinalizeFeatureOnFile", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result


@_dispatch.add_fallback_dispatch_list
@_dispatch.add_type_based_api_dispatcher
@tf_export('yggdrasil_decision_forests_set_logging_level')
def yggdrasil_decision_forests_set_logging_level(level, name=None):
  r"""TODO: add doc.

  Args:
    level: An `int`.
    name: A name for the operation (optional).

  Returns:
    The created Operation.
  """
  _ctx = _context._context or _context.context()
  tld = _ctx._thread_local_data
  if tld.is_eager:
    try:
      _result = pywrap_tfe.TFE_Py_FastPathExecute(
        _ctx, "YggdrasilDecisionForestsSetLoggingLevel", name, "level", level)
      return _result
    except _core._NotOkStatusException as e:
      _ops.raise_from_not_ok_status(e, name)
    except _core._FallbackException:
      pass
    try:
      _result = _dispatcher_for_yggdrasil_decision_forests_set_logging_level(
          (level, name,), None)
      if _result is not NotImplemented:
        return _result
      return yggdrasil_decision_forests_set_logging_level_eager_fallback(
          level=level, name=name, ctx=_ctx)
    except _core._SymbolicException:
      pass  # Add nodes to the TensorFlow graph.
    except (TypeError, ValueError):
      _result = _dispatch.dispatch(
            yggdrasil_decision_forests_set_logging_level, (), dict(level=level,
                                                                   name=name)
          )
      if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
        return _result
      raise
  else:
    _result = _dispatcher_for_yggdrasil_decision_forests_set_logging_level(
        (level, name,), None)
    if _result is not NotImplemented:
      return _result
  # Add nodes to the TensorFlow graph.
  level = _execute.make_int(level, "level")
  try:
    _, _, _op, _outputs = _op_def_library._apply_op_helper(
        "YggdrasilDecisionForestsSetLoggingLevel", level=level, name=name)
  except (TypeError, ValueError):
    _result = _dispatch.dispatch(
          yggdrasil_decision_forests_set_logging_level, (), dict(level=level,
                                                                 name=name)
        )
    if _result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return _result
    raise
  return _op
YggdrasilDecisionForestsSetLoggingLevel = tf_export("raw_ops.YggdrasilDecisionForestsSetLoggingLevel")(_ops.to_raw_op(yggdrasil_decision_forests_set_logging_level))
_dispatcher_for_yggdrasil_decision_forests_set_logging_level = yggdrasil_decision_forests_set_logging_level._tf_type_based_dispatcher.Dispatch


def yggdrasil_decision_forests_set_logging_level_eager_fallback(level, name, ctx):
  level = _execute.make_int(level, "level")
  _inputs_flat = []
  _attrs = ("level", level)
  _result = _execute.execute(b"YggdrasilDecisionForestsSetLoggingLevel", 0,
                             inputs=_inputs_flat, attrs=_attrs, ctx=ctx,
                             name=name)
  _result = None
  return _result

