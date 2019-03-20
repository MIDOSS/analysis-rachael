
clear all; close all;
%%%%%%%set the time steps need to be converted
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
file='I:\Vancouver 2016\vancouver Harbour MOHID\nemo data\bathymetry.nc'; %%%Bathymetry file

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
%%%%%%%%%%create the grid and bathymetry file for MOHID
fid=fopen('I:\Vancouver 2016\vancouver Harbour MOHID\map\data\ST_georgia_bathymetry_revisit.dat','wt');
fprintf(fid,'%s\n','COORD_TIP     : 4');
fprintf(fid,'%s\n',['ILB_IUB       : 1 ',bbb]);
fprintf(fid,'%s\n',['JLB_JUB       : 1 ',aaa]);
fprintf(fid,'%s\n','LATITUDE      : 0');
fprintf(fid,'%s\n','LONGITUDE     : 0');
fprintf(fid,'%s\n','GRID_ANGLE    : 0');
fprintf(fid,'%s',['ORIGIN        : ',start_lon,' ',start_lat]);
fprintf(fid,'%s\n','');
fprintf(fid,'%s','FILL_VALUE    : -99.00');
fprintf(fid,'%s\n','');
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%write XX,  YY
fprintf(fid,'%s\n','<CornersXY>');

for y=1:bb-1;
    for x=1:aa-1;
    fprintf(fid,'%f',grid_lon(x,y));
    fprintf(fid,'%s',' ');
    fprintf(fid,'%f',grid_lat(x,y));     
    fprintf(fid,'%s\n','');
    end
end;
fprintf(fid,'%s\n','<\CornersXY>');
fprintf(fid,'%s\n','');
%%%%%%%%%%%%%%%new%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
depth=ncread(file,'bathymetry',[2,2],[396,896]);


%idz=find(depth==0);
idq=find(isnan(depth));
%depth(idz)=-99;
depth(idq)=-99;
%%%% set up open boundaries (particles can go out of the domain through 
%%%% boundaries when you set the boundary to 0)
idl=find(depth(:,1)~=-99);
depth(idl,1)=0;
idr=find(depth(:,bb-2)~=-99);
depth(idr,bb-2)=0;
idu=find(depth(1,:)~=-99);
depth(1,idu)=0;
idd=find(depth(aa-2,:)~=-99);
depth(aa-2,idd)=0;
depth(394,:)=-99;
fprintf(fid,'%s\n','<BeginGridData2D>');

for y=1:bb-2;
    for x=1:aa-2;
        fprintf(fid,'%f\n',depth(x,y));
    end;
end;
fprintf(fid,'%s\n','<EndGridData2D>');

fclose(fid);


%%