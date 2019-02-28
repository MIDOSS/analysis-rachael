file1=['C:\Users\Shihan Li\Documents\Mohid Studio\Projects\halifax\res\Lagrangian_5.hdf5']; 

for t=1:238;
    tt=num2str(t,'%03d')
    parstr=['/Results/OilSpill/Particle State/Particle State_00',tt];
    lonstr=['/Results/OilSpill/Longitude/Longitude_00',tt];
    latstr=['/Results/OilSpill/Latitude/Latitude_00',tt];
    par_state=h5read(file1,parstr);
    iwc=find(par_state==1.0);
    isu=find(par_state==5.0);
    ibe=find(par_state==10.0);
lon=h5read(file1,lonstr);
lat=h5read(file1,latstr);
lon=double(lon);
lat=double(lat);
lon1=lon(iwc);
lat1=lat(iwc);

lon2=lon(isu);
lat2=lat(isu);

lon3=lon(ibe);
lat3=lat(ibe);

m_proj('Equidistant Cylindrical','lat',[44.52 44.75],'lon',[-63.7 -63.44]);


m_plot(lon2,lat2,'.','MarkerEdgeColor',[0 1 0],'MarkerSize',4);
hold on;

m_plot(lon1,lat1,'.','MarkerEdgeColor',[0 0 1],'MarkerSize',5);
hold on;
m_plot(lon3,lat3,'.','MarkerEdgeColor',[1 1 0],'MarkerSize',4);
hold on;
m_gshhs_f('patch',[.5 .5 .5],'edgecolor','none');
m_grid('tickdir','out','yaxislocation','right',...
       'xaxislocation','top','xlabeldir','end','ticklen',.02);
%M=getframe(gcf);
M(t)=getframe;

end;
movie2avi(M , 'test3.avi', 'compression','None','fps',5);
