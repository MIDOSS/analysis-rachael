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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all; close all;
%%%%%%%set the time steps need to be converted
time=30;
%%%%%%%%%%%Set the start time of hdf5
date_begin=datenum(2018,4,1,23,30,00);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
file='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\bathymetry.nc'; %%%Bathymetry file

file1='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\u_07.nc'; %%%Current U
file2='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\v_07.nc'; %%%Current V
file3='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\grid.nc';
file11='C:\work\data sample\SoG Currents\WC3_CU60_20020101_20020110_grid_U.nc';
lon1=double(ncread(file,'longitude'));%%% grid center lon lat
lat1=double(ncread(file,'latitude'));
 
aa=398;bb=898;cc=40;  %%%% NEMO grid dimension

aaa=num2str(aa-2,'%03d'); 
bbb=num2str(bb-2,'%03d');
ccc=num2str(cc,'%03d');

%%%% set up grid for MOHID (MOHID grid dimensions are 1 longer than its data)
for x=1:aa-1;
    for y=1:bb-1;
        grid_lon(x,y)=(lon1(x,y)+lon1(x,y+1)+lon1(x+1,y+1)+lon1(x+1,y))/4;
        grid_lat(x,y)=(lat1(x,y)+lat1(x,y+1)+lat1(x+1,y+1)+lat1(x+1,y))/4;
    end
end
 
%%%% new grid center lon lat in MOHID (one line of data are abandoned at 
%%%% right, left, top, and bottom respectively, due to the different grid in MOHID)
data_lon(1:aa-2,1:bb-2)=lon1(2:aa-1,2:bb-1);
data_lat(1:aa-2,1:bb-2)=lat1(2:aa-1,2:bb-1);

da_lon=permute(data_lon,[2,1]);
da_lat=permute(data_lat,[2,1]);

%%%% MOHID and NEMO have different directions for data
chunk_size_2D=[bb-2,aa-2];
chunk_size_3D=[bb-2,aa-2,cc];
start_lon=num2str(grid_lon(1,1),'%8f');
start_lat=num2str(grid_lat(1,1),'%8f');
%%



%%

%%%%%%%%%%%%%create hdf5 current files
dataname=('I:\MOHID test data\hdf\e3t_1day_test_0.hdf5');
fid = H5F.create(dataname);
plist = 'H5P_DEFAULT';
%%%%%%%%%%%%create groups in hdf5 based on the MOHID format
gid = H5G.create(fid,'/Results',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Results/vvl',plist,plist,plist);

H5G.close(gid);
gid = H5G.create(fid,'/Time',plist,plist,plist);
H5G.close(gid);
H5F.close(fid);

%%%%%%%%%%%%%%write group attitude
fid=(dataname);

h5writeatt(fid,'/Results','Minimum',0);
h5writeatt(fid,'/Results','Maximum',200);
h5writeatt(fid,'/Results/vvl','Minimum',0);
h5writeatt(fid,'/Results/vvl','Maximum',200);

h5writeatt(fid,'/Time','Minimum',-0.000000);
h5writeatt(fid,'/Time','Maximum',2016.000000);
disp('group created')



for t=1:time;
  
   
    date=datevec(date_begin+(t-1)/24);
    if date(4)==23;
        dddd=date(3);
    ddd=num2str(date(3),'%02d');
    else;
        dddd=date(3)-1;
    ddd=num2str(date(3)-1,'%02d');
    end;
    ref=t-(dddd-1)*24;
    
      disp([t,dddd,ref])
    
    time_counter=num2str(t,'%05d');
    directory=['/Time/Time_',time_counter];
    h5create(fid,directory,6,'ChunkSize',6,'Deflate',6);
    h5writeatt(fid,directory,'Minimum',-0.000000);
    h5writeatt(fid,directory,'Maximum',2020.000000);
    h5writeatt(fid,directory,'Units','YYYY/MM/DD HH:MM:SS');
    h5write(fid,directory,date);

%%%%%%%%%%%%loop for write uv by time

    diru=['C:\Users\Shihan Li\Desktop\SalishSea_1d_20171201_20171201_carp_T.nc'];


    et31=ncread(diru,'e3t',[2,2,1,ref],[aa-2,bb-2,cc,1]);

    
        


%%%%%%%%%%%%%%%%% apply u v at cell center

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%     
    e3t3=permute(e3t1,[2,1,3]);

    e3tt=flip(e3t3,3);

    idu=find(isnan(e3tt));
    e3tt(idu)= 0;

%%%%%%%%%%%%%%%%%%%%%%%
   
   directory=['/Results/vvl/vvl_',time_counter];
   h5create(fid,directory,chunk_size_3D,'ChunkSize',chunk_size_3D,'Deflate',6);
   h5writeatt(fid,directory,'Minimum',0);
   h5writeatt(fid,directory,'Maximum',200);
   h5writeatt(fid,directory,'Units','m');
   h5writeatt(fid,directory,'FillValue',0);
   h5write(fid,directory,e3tt);


 
end

