module potential

  implicit none

  double precision, allocatable :: theta0_(:,:)
  double precision, allocatable :: K_(:,:)

contains

  subroutine setup(exponent, theta0, K)
    integer, intent(in) :: exponent
    double precision, intent(in) :: R0(:,:), K(:,:)
    if (allocated(R0_).and.allocated(K_)) return
    allocate(theta0_(size(theta0,1),size(theta0,2)), source=theta0)
    allocate(K_(size(K,1),size(K,2)), source=K)
  end subroutine setup
  
  subroutine compute(isp,jsp,ksp,rij_sq,rik_sq,cos_theta_ijk,u,w,h)
    integer,          intent(in)    :: isp, jsp, ksp
    double precision, intent(in)    :: rsq_ij, rsq_ik, cos_theta_ijk
    double precision, intent(inout) :: u, w, h
    double precision :: r
    r = sqrt(rsq)
    theta = acos(cos_theta_ijk)
    u = 0.5d0 * K_(isp,jsp) * (theta - theta0_(isp,jsp,ksp))**2
    w = 0.0
    h = 0.0
  end subroutine compute
  
end module potential
