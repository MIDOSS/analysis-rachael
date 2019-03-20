
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
time=384;
%%%%%%%%%%%Set the start time of hdf5
date_begin=datenum(2015,4,7,00,00,00);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
file='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\bathymetry.nc'; %%%Bathymetry file
 
%file='K:\Data\scotian shelf\OUTPUT_SCOTIAN\mesh_mask.nc';
file1='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\u_07.nc'; %%%Current U
file2='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\v_07.nc'; %%%Current V
%file2='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\w_7.nc'; 
file3='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\grid.nc';
 file11='C:\work\data sample\SoG Currents\WC3_CU60_20020101_20020110_grid_U.nc';
% file22='C:\work\data sample\SoG Currents\WC3_CU60_20020101_20020110_grid_V.nc';
 lon1=double(ncread(file,'longitude'));%%% grid center lon lat
 lat1=double(ncread(file,'latitude'));
 
 
 
  
% lon1=double(ncread(file3,'glamt'));%%% grid center lon lat
% lat1=double(ncread(file3,'gphit'));
% lon2=double(ncread(file3,'glamu'));%%% U grid  lon lat
% lat2=double(ncread(file3,'gphiu'));
% lon3=double(ncread(file3,'glamv'));%%% V grid  lon lat
% lat3=double(ncread(file3,'gphiv'));
 
% lon2=double(ncread(file11,'nav_lon'));%%% U grid  lon lat
% lat2=double(ncread(file11,'nav_lat'));
% lon3=double(ncread(file22,'nav_lon'));%%% V grid  lon lat
% lat3=double(ncread(file22,'nav_lat'));
 
 
 
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
%%%%%%%%%%create the grid and bathymetry file for MOHID
% % fid=fopen('I:\Vancouver 2016\vancouver Harbour MOHID\map\data\ST_georgia_bathymetry_final.dat','wt');
% % fprintf(fid,'%s\n','COORD_TIP     : 4');
% % fprintf(fid,'%s\n',['ILB_IUB       : 1 ',bbb]);
% % fprintf(fid,'%s\n',['JLB_JUB       : 1 ',aaa]);
% % fprintf(fid,'%s\n','LATITUDE      : 0');
% % fprintf(fid,'%s\n','LONGITUDE     : 0');
% % fprintf(fid,'%s\n','GRID_ANGLE    : 0');
% % fprintf(fid,'%s',['ORIGIN        : ',start_lon,' ',start_lat]);
% % fprintf(fid,'%s\n','');
% % fprintf(fid,'%s','FILL_VALUE    : -99.00');
% % fprintf(fid,'%s\n','');
% %  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%write XX,  YY
% % fprintf(fid,'%s\n','<CornersXY>');
% % 
% % for y=1:bb-1;
% %     for x=1:aa-1;
% %     fprintf(fid,'%f',grid_lon(x,y));
% %     fprintf(fid,'%s',' ');
% %     fprintf(fid,'%f',grid_lat(x,y));     
% %     fprintf(fid,'%s\n','');
% %     end
% % end;
% % fprintf(fid,'%s\n','<\CornersXY>');
% % fprintf(fid,'%s\n','');
% % 
% % depth=ncread(file,'bathymetry');
% % depth2=griddata(lon1,lat1,depth,data_lon,data_lat);
% % %idz=find(depth==0);
% % idq=find(isnan(depth));
% % %depth(idz)=-99;
% % depth(idq)=-99;
% % %%%% set up open boundaries (particles can go out of the domain through 
% % %%%% boundaries when you set the boundary to 0)
% % idl=find(depth(:,1)~=-99);
% % depth(idl,1)=0;
% % idr=find(depth(:,bb-2)~=-99);
% % depth(idr,bb-2)=0;
% % idu=find(depth(1,:)~=-99);
% % depth(1,idu)=0;
% % idd=find(depth(aa-2,:)~=-99);
% % depth(aa-2,idd)=0;
% % depth(394,:)=-99;
% % fprintf(fid,'%s\n','<BeginGridData2D>');
% % 
% % for y=1:bb-2;
% %     for x=1:aa-2;
% %         fprintf(fid,'%f\n',depth(x,y));
% %     end;
% % end;
% % fprintf(fid,'%s\n','<EndGridData2D>');
% % 
% % fclose(fid);
 
 
%%
 
%%%%%%%%%%%%%create hdf5 current files
dataname=('I:\Vancouver 2016\vancouver Harbour MOHID\nemo current\data\St_georgia_wave5.hdf5');
fid = H5F.create(dataname);
plist = 'H5P_DEFAULT';
%%%%%%%%%%%%create groups in hdf5 based on the MOHID format
gid = H5G.create(fid,'/Results',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Results/mean wave period',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Results/significant wave height',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Results/whitecap coverage',plist,plist,plist);
H5G.close(gid);
gid = H5G.create(fid,'/Time',plist,plist,plist);
H5G.close(gid);
H5F.close(fid);
 
%%%%%%%%%%%%%%write group attitude
fid=(dataname);
 
h5writeatt(fid,'/Results','Minimum',-1e5);
h5writeatt(fid,'/Results','Maximum',1e5);
h5writeatt(fid,'/Results/mean wave period','Minimum',0);
h5writeatt(fid,'/Results/mean wave period','Maximum',1e5);
h5writeatt(fid,'/Results/significant wave height','Minimum',-100);
h5writeatt(fid,'/Results/significant wave height','Maximum',100);
h5writeatt(fid,'/Results/whitecap coverage','Minimum',0);
h5writeatt(fid,'/Results/whitecap coverage','Maximum',1);
h5writeatt(fid,'/Time','Minimum',0.000000);
h5writeatt(fid,'/Time','Maximum',2019.000000);
disp('group created')
 
 
%%%%%%% water level (I just use 0 water level here, please 
%%%%%%% modify it with waterlevel data from model, if you have one)
% u_temp=ncread(file1,'uVelocity',[2,2,1,1],[aa-2,bb-2,1,1]);
% u_temp2=permute(u_temp,[2,1]);
waterlevel(1:bb-2,1:aa-2)=0.0;
% idl=find(u_temp2(:,:)==0);
%waterlevel(idl)=0;
filen='I:\Vancouver 2016\vancouver Harbour MOHID\wave\SoG_ww3_fields_20180407_20180407.nc';
    lon_w(:,1)=ncread(filen,'longitude',[1],[572]);
    lat_w(1,:)=ncread(filen,'latitude',[1],[661]);
    for oo=1:661;
        lon_ww(:,oo)=lon_w;
    end
    for oo=1:572;
        lat_ww(oo,:)=lat_w;
    end
        lon_ww=double(lon_ww)-360;
        lat_ww=double(lat_ww);
        
    
 
%%%%%%%%%%%%Write u v to the hdf5
for t=1:time;
  
   
    date=datevec(date_begin+(t-1)/48);
    dddd=date(3);
    ddd=num2str(date(3),'%02d');
% %     if date(4)==23;
% %         dddd=date(3);
% %     ddd=num2str(date(3),'%02d');
% %     else;
% %         dddd=date(3)-1;
% %     ddd=num2str(date(3)-1,'%02d');
% %     end;
    ref=t-(dddd-7)*48;
    
      disp([t,dddd,ref])
   
    time_counter=num2str(t,'%05d');
    directory=['/Time/Time_',time_counter];
    h5create(fid,directory,6,'ChunkSize',6,'Deflate',6);
    h5writeatt(fid,directory,'Minimum',-0.000000);
    h5writeatt(fid,directory,'Maximum',2016.000000);
    h5writeatt(fid,directory,'Units','YYYY/MM/DD HH:MM:SS');
    h5write(fid,directory,date);
 
%%%%%%%%%%%%loop for write uv by time
 
    diru=['I:\Vancouver 2016\vancouver Harbour MOHID\wave\SoG_ww3_fields_201804',ddd,'_201804',ddd,'.nc'];
 
  
    hs=ncread(diru,'hs',[1,1,ref],[572,661,1]);
    t02=ncread(diru,'t02',[1,1,ref],[572,661,1]);
    wcc=ncread(diru,'wcc',[1,1,ref],[572,661,1]);
 
    
    hs_1=griddata(lon_ww,lat_ww,hs,da_lon,da_lat);
    t02_1=griddata(lon_ww,lat_ww,t02,da_lon,da_lat);
    wcc_1=griddata(lon_ww,lat_ww,wcc,da_lon,da_lat);
 
    idu=find(isnan(hs_1));
    hs_1(idu)=0;
    
     idv=find(isnan(t02_1));
    t02_1(idv)=0;
        
     idw=find(isnan(wcc_1));
    wcc_1(idw)=0;
 
%%%%%%%%%%%%%%%%% method 2: interpolation with griddata, will take longer 
%%%%%%%%%%%%%%%%% time to calculate
% %    for z=1:52;
% %      tr=53-z;
% %      u2(:,:)=(u1(:,:,tr));
% %      v2(:,:)=(v1(:,:,tr));
% %      interp_u(:,:,z)=griddata(lon2,lat2,u2(:,:),data_lon,data_lat);
% %      interp_v(:,:,z)=griddata(lon3,lat3,v2(:,:),data_lon,data_lat);
% %    end;
% %    uu=permute(interp_u,[2,1,3]);
% %    vv=permute(interp_v,[2,1,3]);
   
   directory=['/Results/mean wave period/mean wave period_',time_counter];
   h5create(fid,directory,chunk_size_2D,'ChunkSize',chunk_size_2D,'Deflate',6);
   h5writeatt(fid,directory,'Minimum',0);
   h5writeatt(fid,directory,'Maximum',1e5);
   h5writeatt(fid,directory,'Units','s');
   h5writeatt(fid,directory,'FillValue',0);
   h5write(fid,directory,t02_1);
 
 
   directory=['/Results/significant wave height/significant wave height_',time_counter];
   h5create(fid,directory,chunk_size_2D,'ChunkSize',chunk_size_2D,'Deflate',6);
   h5writeatt(fid,directory,'Minimum',-100);
   h5writeatt(fid,directory,'Maximum',100);
   h5writeatt(fid,directory,'Units','m');
   h5writeatt(fid,directory,'FillValue',0);
   h5write(fid,directory,hs_1);
   
   
      directory=['/Results/whitecap coverage/whitecap coverage_',time_counter];
   h5create(fid,directory,chunk_size_2D,'ChunkSize',chunk_size_2D,'Deflate',6);
   h5writeatt(fid,directory,'Minimum',0);
   h5writeatt(fid,directory,'Maximum',1);
   h5writeatt(fid,directory,'Units','1');
   h5writeatt(fid,directory,'FillValue',0);
   h5write(fid,directory,wcc_1);
 
end
 
