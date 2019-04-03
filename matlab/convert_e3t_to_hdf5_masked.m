%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This program will generate a new e3t.hdf5 file from NEMO output
% from /results2/SalishSea/nowcast-green.201806/
%
% This version corrects a problem created by differences in land mask between NEMO and
% MOHID by incorporating land mask from Salinity file (can use temperature
% or NEMO mask as well)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all; close all;
%%%%%%% set the time steps need to be converted
time=168;

aa=398;bb=898;cc=40;  %%%% NEMO grid dimension
aaa=num2str(aa-2,'%03d');
bbb=num2str(bb-2,'%03d');
ccc=num2str(cc,'%03d');

%%%%%%%%%%%%%create hdf5 current files
dataname=('I:\MOHID test data\hdf\e3t_3.hdf5'); % output HDF5
datao=('I:\UBC file\e3t.hdf5'); % input HDF5
datat=('I:\UBC file\\t.hdf5');  % salinity, temperature and SSH at t-points
fid = H5F.create(dataname);
plist = 'H5P_DEFAULT';

%%%%%%%%%%%%create groups in hdf5 based on the MOHID format
gid = H5G.create(fid,'/Results',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Results/e3t',plist,plist,plist);

H5G.close(gid);
gid = H5G.create(fid,'/Time',plist,plist,plist);
H5G.close(gid);
H5F.close(fid);

%%%%%%%%%%%%%%write group attitude
fid=(dataname);

h5writeatt(fid,'/Results','Minimum',0);
h5writeatt(fid,'/Results','Maximum',200);
h5writeatt(fid,'/Results/e3t','Minimum',0);
h5writeatt(fid,'/Results/e3t','Maximum',200);

h5writeatt(fid,'/Time','Minimum',-0.000000);
h5writeatt(fid,'/Time','Maximum',2016.000000);
disp('group created')
 
% %%%% MOHID and NEMO have different directions for data
chunk_size_2D=[bb-2,aa-2];
chunk_size_3D=[bb-2,aa-2,cc];
%%

for t=1:time;
  disp(t);
    time_counter=num2str(t,'%05d');
    dirt=['/Time/Time_',time_counter];
    date=h5read(datao,dirt);
    directory=['/Time/Time_',time_counter];
    h5create(fid,directory,6,'ChunkSize',6,'Deflate',6);
    h5writeatt(fid,directory,'Minimum',-0.000000);
    h5writeatt(fid,directory,'Maximum',2020.000000);
    h5writeatt(fid,directory,'Units','YYYY/MM/DD HH:MM:SS');
    h5write(fid,directory,date);

%%%%%%%%%%%%loop for write uv by time

    diru=['/Results/e3t/e3t_',time_counter];
    dirs=['/Results/salinity/salinity_',time_counter];
    
    sal=h5read(datat,dirs); % datat: file location, dirs: Structure in file to locate salinity
    ipx=find(sal~=0);
    sal(ipx)=1;
    mask3d=sal;              % mask with ocean=1 and land=0
    e3t1=h5read(datao,diru); % read the e3t from HDF5 file
    e3t=e3t1.*mask3d;        % mask out land as zero

%%%%%%%%%%%%%%%%% apply u v at cell center

   directory=['/Results/e3t/e3t_',time_counter];
   h5create(fid,directory,chunk_size_3D,'ChunkSize',chunk_size_3D,'Deflate',6);
   h5writeatt(fid,directory,'Minimum',0);
   h5writeatt(fid,directory,'Maximum',200);
   h5writeatt(fid,directory,'Units','m');
   h5writeatt(fid,directory,'FillValue',0);
   h5write(fid,directory,e3t);
 
end
