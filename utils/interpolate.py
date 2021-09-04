__all__ = [
  'deep_interpolate'
]

def deep_interpolate(a, b, p) :
  assert(type(a) == type(b))
  t = type(a)

  if t is list :
    return interpolate_list(a, b, p)

  if t is dict :
    return interpolate_dict(a, b, p)
  
  if t in (int, float) :
    return interpolate_values(a, b, p)

def interpolate_values(a, b, p) :
  return a + p * (b - a)

def interpolate_list(A, B, p) :
  return [
    deep_interpolate(a, b, p)
    for (a, b) in zip(A,B)
  ]

def interpolate_dict(A, B, p) :
  assert set(A.keys()) == set(B.keys())
  
  return {
    k: deep_interpolate(A[k], B[k], p)
    for k in A
  }
