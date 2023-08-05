module potential

  implicit none

  double precision, allocatable :: R0_(:,:)
  double precision, allocatable :: K_(:,:)

contains

  subroutine setup(exponent, R0, K)
    integer, intent(in) :: exponent
    double precision, intent(in) :: R0(:,:), K(:,:)
    if (allocated(R0_).and.allocated(K_)) return
    allocate(R0_(size(R0,1),size(R0,2)), source=R0)
    allocate(K_(size(K,1),size(K,2)), source=K)
  end subroutine setup
  
  subroutine compute(isp,jsp,rsq,u,w,h)
    integer,          intent(in)    :: isp, jsp
    double precision, intent(in)    :: rsq
    double precision, intent(inout) :: u, w, h
    double precision :: r
    r = sqrt(rsq)
    u = 0.5d0 * K_(isp,jsp) * (r - R0_(isp,jsp))**2
    w = K_(isp,jsp) * (r - R0_(isp,jsp)) / r
    h = 0.0
  end subroutine compute
  
end module potential
