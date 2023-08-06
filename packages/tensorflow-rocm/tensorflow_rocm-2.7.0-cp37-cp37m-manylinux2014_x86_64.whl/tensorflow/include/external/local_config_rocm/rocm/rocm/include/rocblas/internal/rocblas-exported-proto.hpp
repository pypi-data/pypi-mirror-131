
// Copyright (C) 2020-2021 Advanced Micro Devices, Inc. All rights reserved.

// Script-generated file -- do not edit

// rocBLAS internal API may change each release. The rocBLAS team strongly advises against its use.

#pragma once

#include "internal/rocblas-types.h"


template <int NB, typename Tex, typename Ta, typename Tx, typename Ty>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_axpy_template(rocblas_handle handle,
                                   rocblas_int    n,
                                   const Ta*      alpha,
                                   rocblas_stride stride_alpha,
                                   Tx             x,
                                   ptrdiff_t      offset_x,
                                   rocblas_int    incx,
                                   rocblas_stride stride_x,
                                   Ty             y,
                                   ptrdiff_t      offset_y,
                                   rocblas_int    incy,
                                   rocblas_stride stride_y,
                                   rocblas_int    batch_count);

template <rocblas_int NB, bool CONJ, typename T, typename U, typename V = T>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_dot_template(rocblas_handle __restrict__ handle,
                                  rocblas_int n,
                                  const U __restrict__ x,
                                  rocblas_int    offsetx,
                                  rocblas_int    incx,
                                  rocblas_stride stridex,
                                  const U __restrict__ y,
                                  rocblas_int    offsety,
                                  rocblas_int    incy,
                                  rocblas_stride stridey,
                                  rocblas_int    batch_count,
                                  T* __restrict__ results,
                                  V* __restrict__ workspace);

template <rocblas_int NB, bool ISBATCHED, typename T, typename S>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_iamax_template(rocblas_handle            handle,
                                    rocblas_int               n,
                                    const T                   x,
                                    rocblas_int               shiftx,
                                    rocblas_int               incx,
                                    rocblas_stride            stridex,
                                    rocblas_int               batch_count,
                                    rocblas_int*              result,
                                    rocblas_index_value_t<S>* workspace);

template <rocblas_int NB, bool ISBATCHED, typename T, typename S>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_iamin_template(rocblas_handle            handle,
                                    rocblas_int               n,
                                    const T                   x,
                                    rocblas_int               shiftx,
                                    rocblas_int               incx,
                                    rocblas_stride            stridex,
                                    rocblas_int               batch_count,
                                    rocblas_int*              result,
                                    rocblas_index_value_t<S>* workspace);

template <rocblas_int NB, bool ISBATCHED, typename Ti, typename To, typename Tex = To>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_nrm2_template(rocblas_handle handle,
                                   rocblas_int    n,
                                   const Ti*      x,
                                   rocblas_int    shiftx,
                                   rocblas_int    incx,
                                   rocblas_stride stridex,
                                   rocblas_int    batch_count,
                                   To*            results,
                                   Tex*           workspace);

template <rocblas_int NB, typename Tex, typename Ta, typename Tx>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_scal_template(rocblas_handle handle,
                                   rocblas_int    n,
                                   const Ta*      alpha,
                                   rocblas_stride stride_alpha,
                                   Tx             x,
                                   rocblas_int    offset_x,
                                   rocblas_int    incx,
                                   rocblas_stride stride_x,
                                   rocblas_int    batch_count);

template <typename To>
ROCBLAS_INTERNAL_DEPRECATION size_t rocblas_internal_gemv_kernel_workspace_size(
    rocblas_operation transA, rocblas_int m, rocblas_int n, rocblas_int batch_count = 1);

template <typename T, typename U, typename V, typename W>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_gemv_template(rocblas_handle    handle,
                                   rocblas_operation transA,
                                   rocblas_int       m,
                                   rocblas_int       n,
                                   const U*          alpha,
                                   rocblas_stride    stride_alpha,
                                   const V*          A,
                                   rocblas_int       offseta,
                                   rocblas_int       lda,
                                   rocblas_stride    strideA,
                                   const V*          x,
                                   rocblas_int       offsetx,
                                   rocblas_int       incx,
                                   rocblas_stride    stridex,
                                   const U*          beta,
                                   rocblas_stride    stride_beta,
                                   W*                y,
                                   rocblas_int       offsety,
                                   rocblas_int       incy,
                                   rocblas_stride    stridey,
                                   rocblas_int       batch_count,
                                   T*                workspace = nullptr);

template <bool CONJ, typename T, typename U, typename V, typename W>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_ger_template(rocblas_handle handle,
                                  rocblas_int    m,
                                  rocblas_int    n,
                                  const W*       alpha,
                                  rocblas_stride stride_alpha,
                                  const U*       x,
                                  rocblas_int    offsetx,
                                  rocblas_int    incx,
                                  rocblas_int    stridex,
                                  const U*       y,
                                  rocblas_int    offsety,
                                  rocblas_int    incy,
                                  rocblas_int    stridey,
                                  V*             A,
                                  rocblas_int    offsetA,
                                  rocblas_int    lda,
                                  rocblas_int    strideA,
                                  rocblas_int    batch_count);

template <typename To>
ROCBLAS_INTERNAL_DEPRECATION size_t
    rocblas_internal_hemv_symv_kernel_workspace_size(rocblas_int n, rocblas_int batch_count = 1);

template <bool IS_HEMV, typename U, typename V, typename TPtr, typename W>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_hemv_symv_template(rocblas_handle handle,
                                        rocblas_fill   uplo,
                                        rocblas_int    n,
                                        const U*       alpha,
                                        rocblas_stride stride_alpha,
                                        V              A,
                                        rocblas_int    offseta,
                                        rocblas_int    lda,
                                        rocblas_stride strideA,
                                        V              x,
                                        rocblas_int    offsetx,
                                        rocblas_int    incx,
                                        rocblas_stride stridex,
                                        const U*       beta,
                                        rocblas_stride stride_beta,
                                        TPtr           y,
                                        rocblas_int    offsety,
                                        rocblas_int    incy,
                                        rocblas_stride stridey,
                                        rocblas_int    batch_count,
                                        W              workspace);

template <typename TScal, typename TConstPtr, typename TPtr>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_her2_template(rocblas_handle handle,
                                   rocblas_fill   uplo,
                                   rocblas_int    n,
                                   TScal          alpha,
                                   TConstPtr      x,
                                   rocblas_int    offset_x,
                                   rocblas_int    incx,
                                   rocblas_stride stride_x,
                                   TConstPtr      y,
                                   rocblas_int    offset_y,
                                   rocblas_int    incy,
                                   rocblas_stride stride_y,
                                   TPtr           A,
                                   rocblas_int    lda,
                                   rocblas_int    offset_A,
                                   rocblas_stride stride_A,
                                   rocblas_int    batch_count);

template <typename T, typename U, typename V, typename TPtr, typename W>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_symv_template(rocblas_handle handle,
                                   rocblas_fill   uplo,
                                   rocblas_int    n,
                                   const V*       alpha,
                                   rocblas_stride stride_alpha,
                                   const U*       A,
                                   rocblas_int    offseta,
                                   rocblas_int    lda,
                                   rocblas_stride strideA,
                                   const U*       x,
                                   rocblas_int    offsetx,
                                   rocblas_int    incx,
                                   rocblas_stride stridex,
                                   const V*       beta,
                                   rocblas_stride stride_beta,
                                   TPtr*          y,
                                   rocblas_int    offsety,
                                   rocblas_int    incy,
                                   rocblas_stride stridey,
                                   rocblas_int    batch_count,
                                   W              workspace);

template <typename T, typename U, typename V, typename W>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_syr_template(rocblas_handle handle,
                                  rocblas_fill   uplo,
                                  rocblas_int    n,
                                  U              alpha,
                                  rocblas_stride stride_alpha,
                                  V              x,
                                  rocblas_int    offsetx,
                                  rocblas_int    incx,
                                  rocblas_stride stridex,
                                  W              A,
                                  rocblas_int    offseta,
                                  rocblas_int    lda,
                                  rocblas_stride strideA,
                                  rocblas_int    batch_count);

template <typename TScal, typename TConstPtr, typename TPtr>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_syr2_template(rocblas_handle handle,
                                   rocblas_fill   uplo,
                                   rocblas_int    n,
                                   TScal          alpha,
                                   TConstPtr      x,
                                   rocblas_int    offset_x,
                                   rocblas_int    incx,
                                   rocblas_stride stride_x,
                                   TConstPtr      y,
                                   rocblas_int    offset_y,
                                   rocblas_int    incy,
                                   rocblas_stride stride_y,
                                   TPtr           A,
                                   rocblas_int    lda,
                                   rocblas_int    offset_A,
                                   rocblas_stride stride_A,
                                   rocblas_int    batch_count);

template <typename A, typename X, typename W>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_trmv_template(rocblas_handle    handle,
                                   rocblas_fill      uplo,
                                   rocblas_operation transA,
                                   rocblas_diagonal  diag,
                                   rocblas_int       m,
                                   A                 a,
                                   ptrdiff_t         offseta,
                                   rocblas_int       lda,
                                   rocblas_stride    stridea,
                                   X                 x,
                                   ptrdiff_t         offsetx,
                                   rocblas_int       incx,
                                   rocblas_stride    stridex,
                                   W                 workspace,
                                   rocblas_stride    stridew,
                                   rocblas_int       batch_count);

template <rocblas_int BLOCK, bool BATCHED, typename T, typename U, typename MEM>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_trsv_template_mem(rocblas_handle handle,
                                       rocblas_int    m,
                                       rocblas_int    batch_count,
                                       MEM&           mem,
                                       void*&         mem_x_temp,
                                       void*&         mem_x_temp_arr,
                                       void*&         mem_invA,
                                       void*&         mem_invA_arr,
                                       const U*       supplied_invA      = nullptr,
                                       rocblas_int    supplied_invA_size = 0);

template <rocblas_int BLOCK, bool BATCHED, typename T, typename U, typename V>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_trsv_template(rocblas_handle    handle,
                                   rocblas_fill      uplo,
                                   rocblas_operation transA,
                                   rocblas_diagonal  diag,
                                   rocblas_int       m,
                                   U                 A,
                                   rocblas_int       offset_A,
                                   rocblas_int       lda,
                                   rocblas_stride    stride_A,
                                   V                 B,
                                   rocblas_int       offset_B,
                                   rocblas_int       incx,
                                   rocblas_stride    stride_B,
                                   rocblas_int       batch_count,
                                   void*             x_temp,
                                   void*             x_temparr,
                                   void*             invA               = nullptr,
                                   void*             invAarr            = nullptr,
                                   U                 supplied_invA      = nullptr,
                                   rocblas_int       supplied_invA_size = 0,
                                   rocblas_int       offset_invA        = 0,
                                   rocblas_stride    stride_invA        = 0);

template <rocblas_int DIM_X, typename T, typename ATYPE, typename XTYPE>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_trsv_substitution_template(rocblas_handle    handle,
                                                rocblas_fill      uplo,
                                                rocblas_operation transA,
                                                rocblas_diagonal  diag,
                                                rocblas_int       m,
                                                ATYPE             dA,
                                                ptrdiff_t         offset_A,
                                                rocblas_int       lda,
                                                rocblas_stride    stride_A,
                                                XTYPE             dx,
                                                ptrdiff_t         offset_x,
                                                rocblas_int       incx,
                                                rocblas_stride    stride_x,
                                                rocblas_int       batch_count,
                                                rocblas_int*      w_completed_sec);

template <bool BATCHED, typename T, typename U, typename V>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_gemm_template(rocblas_handle    handle,
                                   rocblas_operation trans_a,
                                   rocblas_operation trans_b,
                                   rocblas_int       m,
                                   rocblas_int       n,
                                   rocblas_int       k,
                                   const T*          alpha,
                                   const U*          A,
                                   rocblas_int       offset_a,
                                   rocblas_int       ld_a,
                                   rocblas_stride    stride_a,
                                   const U*          B,
                                   rocblas_int       offset_b,
                                   rocblas_int       ld_b,
                                   rocblas_stride    stride_b,
                                   const T*          beta,
                                   V*                C,
                                   rocblas_int       offset_c,
                                   rocblas_int       ld_c,
                                   rocblas_stride    stride_c,
                                   rocblas_int       batch_count);

template <bool TWOK, typename TScal, typename TConstPtr, typename UScal, typename TPtr>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_her2k_template(rocblas_handle    handle,
                                    rocblas_fill      uplo,
                                    rocblas_operation trans,
                                    rocblas_int       n,
                                    rocblas_int       k,
                                    TScal             alpha,
                                    TConstPtr         AP,
                                    rocblas_int       offsetA,
                                    rocblas_int       lda,
                                    rocblas_stride    strideA,
                                    TConstPtr         BP,
                                    rocblas_int       offsetB,
                                    rocblas_int       ldb,
                                    rocblas_stride    strideB,
                                    UScal             beta,
                                    TPtr              CP,
                                    rocblas_int       offsetC,
                                    rocblas_int       ldc,
                                    rocblas_stride    strideC,
                                    rocblas_int       batch_count);

template <typename TScal, typename TConstPtr, typename TPtr>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_herk_template(rocblas_handle    handle,
                                   rocblas_fill      uplo,
                                   rocblas_operation transA,
                                   rocblas_int       n,
                                   rocblas_int       k,
                                   TScal             alpha,
                                   TConstPtr         AP,
                                   rocblas_int       offsetA,
                                   rocblas_int       lda,
                                   rocblas_stride    strideA,
                                   TScal             beta,
                                   TPtr              CP,
                                   rocblas_int       offsetC,
                                   rocblas_int       ldc,
                                   rocblas_stride    strideC,
                                   rocblas_int       batch_count);

template <bool HERM, typename TScal, typename TConstPtr, typename TPtr>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_symm_template(rocblas_handle handle,
                                   rocblas_side   side,
                                   rocblas_fill   uplo,
                                   rocblas_int    m,
                                   rocblas_int    n,
                                   TScal          alpha,
                                   TConstPtr      AP,
                                   rocblas_int    offsetA,
                                   rocblas_int    lda,
                                   rocblas_stride strideA,
                                   TConstPtr      BP,
                                   rocblas_int    offsetB,
                                   rocblas_int    ldb,
                                   rocblas_stride strideB,
                                   TScal          beta,
                                   TPtr           CP,
                                   rocblas_int    offsetC,
                                   rocblas_int    ldc,
                                   rocblas_stride strideC,
                                   rocblas_int    batch_count);

template <bool TWOK, typename TScal, typename TConstPtr, typename TPtr>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_syr2k_template(rocblas_handle    handle,
                                    rocblas_fill      uplo,
                                    rocblas_operation trans,
                                    rocblas_int       n,
                                    rocblas_int       k,
                                    TScal             alpha,
                                    TConstPtr         AP,
                                    rocblas_int       offsetA,
                                    rocblas_int       lda,
                                    rocblas_stride    strideA,
                                    TConstPtr         BP,
                                    rocblas_int       offsetB,
                                    rocblas_int       ldb,
                                    rocblas_stride    strideB,
                                    TScal             beta,
                                    TPtr              CP,
                                    rocblas_int       offsetC,
                                    rocblas_int       ldc,
                                    rocblas_stride    strideC,
                                    rocblas_int       batch_count);

template <typename TScal, typename TConstPtr, typename TPtr>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_syrk_template(rocblas_handle    handle,
                                   rocblas_fill      uplo,
                                   rocblas_operation transA,
                                   rocblas_int       n,
                                   rocblas_int       k,
                                   TScal             alpha,
                                   TConstPtr         AP,
                                   rocblas_int       offsetA,
                                   rocblas_int       lda,
                                   rocblas_stride    strideA,
                                   TScal             beta,
                                   TPtr              CP,
                                   rocblas_int       offsetC,
                                   rocblas_int       ldc,
                                   rocblas_stride    strideC,
                                   rocblas_int       batch_count);

template <int  MIN_NB,
          bool BATCHED,
          typename T,
          typename TScal,
          typename TPtr,
          typename TConstPtr,
          typename TLd>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_syrkx_template(rocblas_handle    handle,
                                    rocblas_fill      uplo,
                                    rocblas_operation trans,
                                    rocblas_int       n,
                                    rocblas_int       k,
                                    TScal*            alpha,
                                    TConstPtr*        da,
                                    TLd               offset_a,
                                    TLd               lda,
                                    rocblas_stride    stride_a,
                                    TConstPtr*        db,
                                    TLd               offset_b,
                                    TLd               ldb,
                                    rocblas_stride    stride_b,
                                    TScal*            beta,
                                    TPtr*             dc,
                                    TLd               offset_c,
                                    TLd               ldc,
                                    rocblas_stride    stride_c,
                                    rocblas_int       batch_count);

template <int STOPPING_NB, bool BATCHED, typename T, typename TScal, typename TConstPtr, typename TPtr, typename T_lda>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status rocblas_internal_trmm_recursive_template(rocblas_handle    handle,
                                     rocblas_side      side,
                                     rocblas_fill      uplo,
                                     rocblas_operation trans_a,
                                     rocblas_diagonal  diag,
                                     rocblas_int       m,
                                     rocblas_int       n,
                                     TScal*            alpha,
                                     rocblas_stride    stride_alpha,
                                     TConstPtr*        dA,
                                     T_lda             offset_a,
                                     T_lda             ldda,
                                     rocblas_stride    stride_a,
                                     TPtr*             dB,
                                     T_lda             offset_b,
                                     T_lda             lddb,
                                     rocblas_stride    stride_b,
                                     rocblas_int       batch_count);

template <rocblas_int BLOCK, bool BATCHED, typename T>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_trsm_workspace_size(rocblas_side side,
                                         rocblas_int  m,
                                         rocblas_int  n,
                                         rocblas_int  batch_count,
                                         rocblas_int  supplied_invA_size,
                                         size_t*      w_x_tmp_size,
                                         size_t*      w_x_tmp_arr_size,
                                         size_t*      w_invA_size,
                                         size_t*      w_invA_arr_size,
                                         size_t*      w_x_tmp_size_backup);

template <rocblas_int BLOCK, bool BATCHED, typename T, typename U, typename V>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_trsm_template(rocblas_handle    handle,
                                   rocblas_side      side,
                                   rocblas_fill      uplo,
                                   rocblas_operation transA,
                                   rocblas_diagonal  diag,
                                   rocblas_int       m,
                                   rocblas_int       n,
                                   const T*          alpha,
                                   U                 A,
                                   rocblas_int       offset_A,
                                   rocblas_int       lda,
                                   rocblas_stride    stride_A,
                                   V                 B,
                                   rocblas_int       offset_B,
                                   rocblas_int       ldb,
                                   rocblas_stride    stride_B,
                                   rocblas_int       batch_count,
                                   bool              optimal_mem,
                                   void*             w_x_temp,
                                   void*             w_x_temparr,
                                   void*             invA               = nullptr,
                                   void*             invAarr            = nullptr,
                                   U                 supplied_invA      = nullptr,
                                   rocblas_int       supplied_invA_size = 0,
                                   rocblas_int       offset_invA        = 0,
                                   rocblas_stride    stride_invA        = 0);

template <rocblas_int NB>
ROCBLAS_INTERNAL_DEPRECATION size_t rocblas_internal_trtri_temp_size(rocblas_int n,
                                                                         rocblas_int batch_count);

template <rocblas_int NB, bool BATCHED, bool STRIDED, typename T, typename U, typename V>
ROCBLAS_INTERNAL_DEPRECATION rocblas_status
    rocblas_internal_trtri_template(rocblas_handle   handle,
                                    rocblas_fill     uplo,
                                    rocblas_diagonal diag,
                                    rocblas_int      n,
                                    U                A,
                                    rocblas_int      offset_A,
                                    rocblas_int      lda,
                                    rocblas_stride   stride_A,
                                    rocblas_stride   sub_stride_A,
                                    V                invA,
                                    rocblas_int      offset_invA,
                                    rocblas_int      ldinvA,
                                    rocblas_stride   stride_invA,
                                    rocblas_stride   sub_stride_invA,
                                    rocblas_int      batch_count,
                                    rocblas_int      sub_batch_count,
                                    V                w_C_tmp);

