"""Gaussian chemical blur approximation for Phase 5 Level 1."""

from __future__ import annotations

import math

import numpy as np

from .resist_threshold import threshold_resist


def gaussian_kernel_1d(
    sigma_m: float,
    pixel_size_m: float,
    *,
    truncate: float = 3.0,
) -> np.ndarray:
    """Return a normalized 1-D Gaussian kernel sampled in pixel units."""
    _validate_blur_inputs(sigma_m, pixel_size_m, truncate)
    if sigma_m == 0.0:
        return np.array([1.0], dtype=np.float64)

    sigma_px = sigma_m / pixel_size_m
    radius = max(1, int(math.ceil(truncate * sigma_px)))
    coords = np.arange(-radius, radius + 1, dtype=np.float64)
    kernel = np.exp(-0.5 * (coords / sigma_px) ** 2)
    kernel_sum = float(np.sum(kernel))
    if kernel_sum <= 0.0:
        raise ValueError("Gaussian kernel sum must be positive")
    return (kernel / kernel_sum).astype(np.float64)


def gaussian_blur(
    aerial: np.ndarray,
    pixel_size_m: float,
    sigma_m: float,
    *,
    truncate: float = 3.0,
) -> np.ndarray:
    """Apply separable Gaussian blur to a 1-D or 2-D aerial intensity array."""
    image = np.asarray(aerial, dtype=np.float64)
    if image.ndim not in {1, 2}:
        raise ValueError("aerial must be a 1-D line or 2-D image")
    if image.size == 0:
        raise ValueError("aerial must contain at least one pixel")
    if not np.all(np.isfinite(image)):
        raise ValueError("aerial must contain finite values")
    if np.any(image < 0.0):
        raise ValueError("aerial intensity must be non-negative")

    kernel = gaussian_kernel_1d(sigma_m, pixel_size_m, truncate=truncate)
    if kernel.size == 1:
        return image.copy()

    blurred = _convolve_along_axis(image, kernel, axis=0)
    if image.ndim == 2:
        blurred = _convolve_along_axis(blurred, kernel, axis=1)
    return blurred.astype(np.float64)


def blurred_threshold_resist(
    aerial: np.ndarray,
    pixel_size_m: float,
    sigma_m: float,
    *,
    dose: float = 1.0,
    threshold: float = 0.3,
    truncate: float = 3.0,
) -> np.ndarray:
    """Blur aerial intensity before applying the Phase 5 threshold resist."""
    blurred = gaussian_blur(
        aerial,
        pixel_size_m,
        sigma_m,
        truncate=truncate,
    )
    return threshold_resist(blurred, dose=dose, threshold=threshold)


def transition_width(
    intensity_line: np.ndarray,
    pixel_size_m: float,
    *,
    low: float = 0.1,
    high: float = 0.9,
) -> float:
    """Estimate edge-spread width between low and high normalized intensities."""
    line = np.asarray(intensity_line, dtype=np.float64)
    if line.ndim != 1:
        raise ValueError("intensity_line must be 1-D")
    if line.size == 0:
        raise ValueError("intensity_line must contain at least one pixel")
    if not np.all(np.isfinite(line)):
        raise ValueError("intensity_line must contain finite values")
    if not 0.0 <= low < high <= 1.0:
        raise ValueError("low and high must satisfy 0 <= low < high <= 1")
    if not np.isfinite(pixel_size_m) or pixel_size_m <= 0.0:
        raise ValueError("pixel_size_m must be a positive finite value")

    normalized = line.copy()
    line_min = float(np.min(normalized))
    line_max = float(np.max(normalized))
    span = line_max - line_min
    if span <= 0.0:
        return 0.0
    normalized = (normalized - line_min) / span
    transition = (normalized > low) & (normalized < high)
    return float(np.count_nonzero(transition) * pixel_size_m)


def _convolve_along_axis(
    image: np.ndarray,
    kernel: np.ndarray,
    axis: int,
) -> np.ndarray:
    radius = kernel.size // 2
    pad_width = [(0, 0)] * image.ndim
    pad_width[axis] = (radius, radius)
    padded = np.pad(image, pad_width, mode="edge")
    return np.apply_along_axis(
        lambda line: np.convolve(line, kernel, mode="valid"),
        axis,
        padded,
    )


def _validate_blur_inputs(
    sigma_m: float,
    pixel_size_m: float,
    truncate: float,
) -> None:
    if not np.isfinite(sigma_m) or sigma_m < 0.0:
        raise ValueError("sigma_m must be a non-negative finite value")
    if not np.isfinite(pixel_size_m) or pixel_size_m <= 0.0:
        raise ValueError("pixel_size_m must be a positive finite value")
    if not np.isfinite(truncate) or truncate <= 0.0:
        raise ValueError("truncate must be a positive finite value")
