module interaction_vector

  use helpers
  use cutoff  !, only: is_zero, smooth, tailor
  use potential  !, only: compute
  
  implicit none

contains

  subroutine forces(box,pos,ids,for,epot,virial)
    double precision, intent(in)    :: box(:)
    double precision, intent(in)    :: pos(:,:)
    integer,          intent(in)    :: ids(:)
    double precision, intent(inout) :: for(:,:)
    double precision, intent(out)   :: epot, virial
    double precision                :: rij(size(pos,1)), rijsq, hbox(size(pos,1))
    double precision, allocatable   :: rij_all(:,:), rijsq_all(:), uij(:), wij(:), hij(:)
    integer,          allocatable   :: jsp_all(:), j_all(:)  !size(pos,1),size(pos,2))
    integer                         :: max  !size(pos,2)
    integer                         :: i, j, isp, jsp
    logical                         :: zero_ij
    ! TODO: it should be possible to tailor the cutoff from python, but the compute interface is not parsed correctly
    call tailor(compute)
    allocate(rij_all(size(pos,1),size(pos,2)))
    allocate(rijsq_all(size(pos,2)))
    allocate(jsp_all(size(pos,2)),j_all(size(pos,2)))
    allocate(uij(size(pos,2)),wij(size(pos,2)),hij(size(pos,2)))
    for = 0.0d0
    epot = 0.0d0
    virial = 0.0d0
    hbox = box / 2
    do i = 1,size(pos,2)
       isp = ids(i)
       ! Pack distances within cutoff into arrays
       max = 0
       do j = i+1,size(pos,2)
          jsp = ids(j)
          call distance(i,j,pos,rij)
          call pbc(rij,box,hbox)
          call dot(rij,rij,rijsq)
          call is_zero(isp,jsp,rijsq,zero_ij)          
          if (.not.zero_ij) then
             max = max + 1
             rij_all(:, max) = rij
             rijsq_all(max) = rijsq
             jsp_all(max) = jsp
             j_all(max) = j
          end if
       end do
       ! Vectorized potential calculation
       ! We should ignore inlining (probably we must)
       call compute_vector(isp,jsp_all(1:max),rijsq_all(1:max),uij(1:max),wij(1:max),hij(1:max)) ! wij = -(du/dr)/r
       call smooth_vector(isp,jsp_all(1:max),rijsq_all(1:max),uij(1:max),wij(1:max),hij(1:max)) ! wij = -(du/dr)/r
       ! Reduction
       epot = epot + sum(uij(1:max))
       virial = virial + sum(wij(1:max) * rijsq_all(1:max))
       do j = 1,max
          for(:,i) = for(:,i) - wij(j) * rij_all(:,j)
       end do
       do j = 1,max
          for(:,j_all(j)) = for(:,j_all(j)) - wij(j) * rij_all(:,j)
       end do
    end do
    deallocate(rij_all,jsp_all,rijsq_all,uij,wij,hij)
  end subroutine forces

  subroutine hessian(box,pos,ids,hes)
    double precision, intent(in)    :: box(:)
    double precision, intent(in)    :: pos(:,:)
    integer,          intent(in)    :: ids(:)
    !double precision, intent(inout) :: hes(size(pos,1),size(pos,2),size(pos,1),size(pos,2))
    double precision, intent(inout) :: hes(:,:,:,:)
    double precision                :: rij(size(pos,1)), rijsq, uij, wij, wwij, hbox(size(pos,1))
    double precision                :: unity(size(pos,1),size(pos,1)), mij(size(pos,1),size(pos,1)), mmij(size(pos,1),size(pos,1))
    integer                         :: i, j, isp, jsp
    logical                         :: zero_ij
    call tailor(compute)
    hes = 0.0d0
    unity = 0.0d0
    hbox = box / 2
    do i = 1,size(unity,1)
       unity(i,i) = 1.0d0
    end do
    loop_i: do i = 1,size(pos,2)
       isp = ids(i)
       loop_j: do j = i+1,size(pos,2)          
          jsp = ids(j)
          rij = pos(:,i) - pos(:,j)
          call pbc(rij,box,hbox)
          rijsq = dot_product(rij,rij)
          call is_zero(isp,jsp,rijsq,zero_ij)
          if (.not.zero_ij) then
             call compute(isp,jsp,rijsq,uij,wij,wwij)
             call smooth(isp,jsp,rijsq,uij,wij,wwij)
             mij = unity(:,:) * wij
             mmij = outer_product(rij,rij) * wwij
             ! Diagonal in i,j - diagonal in x,y
             hes(:,i,:,i) = hes(:,i,:,i) - mij
             hes(:,j,:,j) = hes(:,j,:,j) - mij
             ! Off-diagonal in i,j - diagonal in x,y
             hes(:,i,:,j) = hes(:,i,:,j) + mij
             hes(:,j,:,i) = hes(:,j,:,i) + mij
             ! Diagonal in i,j - off-diagonal in x,y
             hes(:,i,:,i) = hes(:,i,:,i) + mmij
             hes(:,j,:,j) = hes(:,j,:,j) + mmij
             ! Off-diagonal in i,j - off-diagonal in x,y
             hes(:,i,:,j) = hes(:,i,:,j) - mmij
             hes(:,j,:,i) = hes(:,j,:,i) - mmij
          end if
       end do loop_j
    end do loop_i
  end subroutine hessian

  subroutine gradw(box,pos,ids,grad_w)
    double precision, intent(in)    :: box(:)
    double precision, intent(in)    :: pos(:,:)
    integer,  intent(in)    :: ids(:)
    double precision, intent(inout) :: grad_w(:,:)
    double precision                :: rij(size(pos,1)), rijsq, uij, wij, wwij
    double precision                :: hbox(size(pos,1)), grwij(size(pos,1)), forc(size(pos,1),size(pos,2)), epot, virial
    integer                 :: i, j, isp, jsp
    logical :: zero_ij
    call tailor(compute)
    call forces(box,pos,ids,forc,epot,virial)
    grad_w = 0.d0
    hbox = box / 2
    loop_i: do i = 1,size(pos,2)
       isp = ids(i)
       loop_j: do j = i+1,size(pos,2)          
          jsp = ids(j)
          call distance(i,j,pos,rij)
          call pbc(rij,box,hbox)
          call dot(rij,rij,rijsq)
          call is_zero(isp,jsp,rijsq,zero_ij)          
          if (.not.zero_ij) then
             call compute(isp,jsp,rijsq,uij,wij,wwij)
             call smooth(isp,jsp,rijsq,uij,wij,wwij)
             ! Signs are reversed compared to f90atooms...
             grwij = wij * forc(:,i) - rij(:) * (wwij * DOT_PRODUCT(rij(:),forc(:,i)))
             grad_w(:,i) = grad_w(:,i) + grwij(:)
             grad_w(:,j) = grad_w(:,j) - grwij(:)
             grwij = wij * forc(:,j) - rij(:) * (wwij * DOT_PRODUCT(rij(:),forc(:,j)))
             grad_w(:,i) = grad_w(:,i) - grwij(:)
             grad_w(:,j) = grad_w(:,j) + grwij(:)
          end if
       end do loop_j
    end do loop_i
    grad_w = grad_w * 2
  end subroutine gradw
  
end module interaction_vector
