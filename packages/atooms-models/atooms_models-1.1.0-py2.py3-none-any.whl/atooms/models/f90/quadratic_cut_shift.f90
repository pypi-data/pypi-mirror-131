module cutoff

  implicit none

  double precision, allocatable :: rcut_(:,:)
  double precision, allocatable :: a_cut(:,:)
  double precision, allocatable :: b_cut(:,:)

contains

  subroutine setup(rcut)
    double precision, intent(in) :: rcut(:,:)
    if (allocated(rcut_)) return
    allocate(rcut_(size(rcut,1),size(rcut,2)), source=rcut)
    allocate(a_cut(size(rcut,1),size(rcut,2)))
    allocate(b_cut(size(rcut,1),size(rcut,2)))
  end subroutine setup

  subroutine is_zero(isp,jsp,rsq,result)
    integer,          intent(in) :: isp, jsp
    double precision, intent(in) :: rsq
    logical,          intent(out) :: result
    result = rsq > rcut_(isp,jsp)**2
  end subroutine is_zero

  subroutine tailor(potential)
    ! note that U'=-u1*radius 
    !   A = - 0.5*U'(r_c)/r_c
    !   B =   0.5*U'(r_c)*r_c - U(r_c) 
    ! so that
    !   U_qs(r) = U(r) + A*r^2 + B
    ! is smooth up to its first derivative at r=r_c
    integer :: isp,jsp,nsp
    double precision :: rcutsq, u, w, h, uu(3)
    interface
       subroutine compute(isp,jsp,rsq,u,w,h)
         integer,          intent(in)  :: isp, jsp
         double precision, intent(in)  :: rsq
         double precision, intent(inout) :: u, w, h
       end subroutine compute
    end interface
    procedure(compute) :: potential
    nsp = size(rcut_)
    if (allocated(a_cut)) return
    if (allocated(b_cut)) return
    allocate(a_cut(nsp,nsp))
    allocate(b_cut(nsp,nsp))
    do isp = 1,nsp
       do jsp = 1,nsp
          ! signature is not guessed correctly, u, w, h are intent(in)
          call potential(isp,jsp,rcutsq,u,w,h)
          a_cut(isp,jsp) =   0.d5 * w
          b_cut(isp,jsp) = - 0.d5 * w * rcut_(isp,jsp)**2 - u
       end do
    end do
  end subroutine tailor

  subroutine smooth(isp,jsp,rsq,uij,wij,hij)
    integer,          intent(in)    :: isp, jsp
    double precision, intent(in)    :: rsq
    double precision, intent(inout) :: uij,wij,hij
    uij = uij + a_cut(isp,jsp) * rsq + b_cut(isp,jsp)
    wij = wij - a_cut(isp,jsp) * 2.d0
    hij = hij
  end subroutine smooth
  
end module cutoff
