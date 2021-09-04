## create_frames.py
## ====================================================
import logging as lg

## Create Frames
## ----------------------------------------------------
def create_frames(args) :
  from . frame import random_frame, frame_dist
  from utils import write_data

  # compute key frames
  nf, nk = args.n_frames, args.n_keyframes
  nk = min(nf, nk)
  frames = [random_frame() for _ in range(nk)]

  # compute rest of the frames
  if nf > nk :
    # compute the count of interpolations required
    counts = interpolation_counts(frames, nf-nk)
    lg.debug('main: interpolation_params: %s', counts)
    # lg.debug(
    #   'main: interpolation_params:\n%s', '\n'.join(
    #     f'{id}: {count}'
    #     for (id, count) in zip(ids, counts)
    #   )
    # )

    interpolated = [
      # interpolate_frames(frames[i0], frames[1i], count)
      # for ((i0, i1), count) in zip(ids, counts)

      interpolate_frames(frames[i], frames[1+i], count)
      for i, count in enumerate(counts)
    ]
    lg.debug('main: (before collate); len(frames): %s, '
             'len(interpolated): %s',
             len(frames), len(interpolated))

    frames = collate(frames, interpolated)
    lg.debug('main: (after collate); len(frames): %s',
             len(frames))

  dist = map(
    frame_dist, frames[:-1], frames[1:]
  )
  lg.debug('main: dist: %s', list(dist))

  write_data(frames, args.output)


## Interpolate
## ====================================================

def interpolate_frames(frame_a, frame_b, n) :
  from utils import deep_interpolate

  if n <= 0 :
    return []

  p = lambda i: (1+i) / (1+n)

  return [
    deep_interpolate(frame_a, frame_b, p(i))
    for i in range(n)
  ]


## Collate
## ====================================================
def collate(frames, interpolated) :
  _frames, last_frame = frames[:-1], frames[-1]
  frames = []

  for frame,inter_frames in zip(_frames, interpolated):
    frames.append(frame)
    frames.extend(inter_frames)

  frames.append(last_frame)

  return frames

## Interpolation Counts
## ====================================================

def interpolation_counts(frames, n) :
  ids, dis = sorted_frame_dist(frames)
  ids, counts = compute_counts(ids, dis, n)
  lg.debug('interpolation_params: counts '
           '(before sorting): %s', counts)

  ids, counts = list(zip(*
    list(sorted(
      zip(ids, counts),
      key = lambda x: x[0][0]
    ))
  ))
  lg.debug('interpolation_params: counts '
           '(after sorting): %s', counts)

  return counts

# Compute interpolation counts from distances
def compute_counts(ids, dis, n) :
  
  z = sum(dis)
  counts = [
    int(round(n * d / z))
    for d in dis
  ]

  if sum(counts) < n :
    # Negative residue
    n_residue = n - sum(counts)
    l = 1 + len(ids)
    counts = [
      counts[i] + 
      n_residue // l +
      int(i > (n_residue % l))

      for i in range(len(ids))
    ]

  if sum(counts) > n :
    # Positive residue
    s = 0
    _counts, counts = counts, []
    for i, c in enumerate(_counts) :
      if s == n :
        # Balanced; append zeros
        counts.append(0)
        continue

      # Residual nature in local
      s += c

      if s > n :
        # Positive residue in local
        p_residue = s - n
        # Counter balance the residue
        s -= p_residue
        c -= p_residue
        
      counts.append(c)

  return ids, counts

def sorted_frame_dist(frames) :
  from . frame import frame_dist

  dist = map(
    frame_dist, frames[:-1], frames[1:]
  )

  nf = len(frames)
  dist_ids = list(zip(
    range(0, nf-1),
    range(1, nf)
  ))

  dist, dist_ids = list(zip(*
    sorted(
      zip(dist, dist_ids),
      key = lambda x: x[0],
      reverse=True
    )
  ))
  lg.debug('sorted_frame_dist: dist: %s', dist)

  return dist_ids, dist
