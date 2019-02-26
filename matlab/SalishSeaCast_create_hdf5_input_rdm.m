
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% This program will generate two files: 
%%% (1) Grid and bathymetry file for MOHID; (If use this generated file 
%%%     in MOHID, the MOHID model could generate a new bathymetry file, 
%%%     automatically, and you need to replace the old one with the new
%%%     one. This process could occur more than one times)
%%% (2) hdf current file used in MOHID; (due to the different methods for
%%%     grid settings in NEMO and MOHID, the variables will have a
%%%     dimension (b-2,a-2,c',t), where (a,b,c,t) is the original dimension
%%%     from NEMO, c' means the order of elements are reversed.
 
 
% Modified (2/1/2019) by RMueller to run on Skookum 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all; close all;

% RDM: inputs
dt     = 24; % output time step
ndays  = 7; % number of days to run model
tstart = datenum(2017,11,28,00,00,00); % Set the start time of hdf5
%nowcast_dir = '/results2/MIDOSS/forcing/SalishSeaCast/nowcast-green/28nov17-05dec17/';
nowcast_dir = '/Users/rmueller/Projects/MIDOSS/analysis-rachael/matlab';
out_dir     = nowcast_dir;

u_fname = '3du.nc';
u_outname = 'SOILED_u.hdf5';

% RDM: Read these from variabl dimension? 
%%%% NEMO grid dimension
nx=398; %aa
ny=898; %bb
nz=40;  %cc

%%%%%%% set the time steps need to be converted
%time=168; %RDM: this is 7 days of hourly output.  Update code so that time is automated
time = dt*ndays;

% RDM: Specify fullfile name for the u, v, T and w output 
u_dir_f = fullfile(nowcast_dir, u_fname); % "file1"
v_dir_f = fullfile(nowcast_dir, v_fname); % "file2"   

%%%%%%%%%%%%%create hdf5 current files
out_dir_f = fullfile(out_dir,u_outname);
fid = H5F.create(out_dir_f);
plist = 'H5P_DEFAULT';

%%%%%%%%%%%%create groups in hdf5 based on the MOHID format
gid = H5G.create(fid,'/Results',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Results/velocity U',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Time',plist,plist,plist);
H5G.close(gid);
H5F.close(fid);
 
%%%%%%%%%%%%%%write group attitude
fid=(out_dir_f);
h5writeatt(fid,'/Results','Minimum',-5);
h5writeatt(fid,'/Results','Maximum',5);
h5writeatt(fid,'/Results/velocity U','Minimum',-5);
h5writeatt(fid,'/Results/velocity U','Maximum',5);
h5writeatt(fid,'/Time','Minimum',-0.000000);
h5writeatt(fid,'/Time','Maximum',2016.000000);
disp('group created')
 
%%%%%%%%%%%%Write u to the hdf5
for t_ind=1:time;
    date=datevec(tstart+(t_ind-1)/24);
    if date(4)==23;
        dddd=date(3);
    ddd=num2str(date(3),'%02d');
    else;
        dddd=date(3)-1;
    ddd=num2str(date(3)-1,'%02d');
    end;
    ref=t_ind-(dddd-7)*24;
    
      disp([t_ind,dddd,ref])
    
    time_counter=num2str(t_ind,'%05d');
    directory=['/Time/Time_',time_counter];
    h5create(fid,directory,6,'ChunkSize',6,'Deflate',6);
    h5writeatt(fid,directory,'Minimum',-0.000000);
    h5writeatt(fid,directory,'Maximum',2016.000000);
    h5writeatt(fid,directory,'Units','YYYY/MM/DD HH:MM:SS');
    h5write(fid,directory,date);
 
%%%%%%%%%%%%loop for write u by time
    u1=ncread(u_dir_f,'uVelocity',[2,2,1,ref],[nx-2,ny-2,nz,1]);
    u2=u1;    
    u3=permute(u2,[2,1,3]);
    uu=flip(u3,3);
    idu=find(isnan(uu));
    uu(idu)=0;
        
  
   directory=['/Results/velocity U/velocity U_',time_counter];
   h5create(fid,directory,chunk_size_3D,'ChunkSize',chunk_size_3D,'Deflate',6);
   h5writeatt(fid,directory,'Minimum',-5);
   h5writeatt(fid,directory,'Maximum',5);
   h5writeatt(fid,directory,'Units','m/s');
   h5writeatt(fid,directory,'FillValue',0);
   h5write(fid,directory,uu);
 
    
end
 
