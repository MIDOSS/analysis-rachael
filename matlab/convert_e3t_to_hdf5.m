%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% This program will generate a new e3t.hdf5 file from NEMO output
% from /results2/SalishSea/nowcast-green.201806/
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


clear all; close all;
%%%%%%%set the time steps need to be converted
time=30;
%%%%%%%%%%%Set the start time of hdf5
date_begin=datenum(2018,4,1,23,30,00);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

aa=398;bb=898;cc=40;  %%%% NEMO grid dimension

aaa=num2str(aa-2,'%03d'); 
bbb=num2str(bb-2,'%03d');
ccc=num2str(cc,'%03d');

%%%%%%%%%%%%% create hdf5 current files
dataname=('I:\MOHID test data\hdf\e3t_1day_test_0.hdf5');


fid = H5F.create(dataname);
plist = 'H5P_DEFAULT';

%%%%%%%%%%%% create groups in hdf5 based on the MOHID format
gid = H5G.create(fid,'/Results',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Results/vvl',plist,plist,plist);

H5G.close(gid);
gid = H5G.create(fid,'/Time',plist,plist,plist);
H5G.close(gid);
H5F.close(fid);

%%%%%%%%%%%%%% write group attitude
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

    diru=['C:\Users\Shihan Li\Desktop\SalishSea_1d_20171201_20171201_carp_T.nc'];

    et31=ncread(diru,'e3t',[2,2,1,ref],[aa-2,bb-2,cc,1]);
    e3t3=permute(e3t1,[2,1,3]);
    e3tt=flip(e3t3,3);

% Set NaN values to zero
    idu=find(isnan(e3tt));
    e3tt(idu)= 0;

% Write e3t values to file  
   directory=['/Results/vvl/vvl_',time_counter];
   h5create(fid,directory,chunk_size_3D,'ChunkSize',chunk_size_3D,'Deflate',6);
   h5writeatt(fid,directory,'Minimum',0);
   h5writeatt(fid,directory,'Maximum',200);
   h5writeatt(fid,directory,'Units','m');
   h5writeatt(fid,directory,'FillValue',0);
   h5write(fid,directory,e3tt);

 
end

