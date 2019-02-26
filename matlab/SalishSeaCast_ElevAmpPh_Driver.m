close all; clear all;

path(path,'/Users/rmueller/toolbox/matlab/ROMS/Tides/PlotTideAmpPhase');
path(path,'/Users/rmueller/toolbox/matlab/TMD_2.01/FUNCTIONS');
path(path, fullfile('/Users/rmueller/toolbox/matlab/Colormaps/cmocean_v1/cmocean'))
cons = {'m2', 's2', 'k1', 'o1','mk3','m4', 'n2','p1','k2','q1'};
cons_fig = {'M_2','S_2','K_1','O_1','MK_3','M_4', 'N_2','P_1','K_2','Q_1'};
%cons = {'n2  ';'p1  ';'k2  ';'q1  '};
%cons_fig = {'N_2','P_1','K_2','Q_1'};

SLAT = '70';SLON = -20; HEMI = 'n';
fs = 12;

% 48hrs of SSH (m) starting from 01/01/2016, OO:30:00Z
his_dir = '/Users/rmueller/Projects/MIDOSS/analysis-rachael/matlab/';
his_ssh = 'ubcSSgSurfaceTracerFields1hV18-06_01012019_40day.nc'; 
his_dir_f = fullfile(his_dir, his_ssh);
tag = 'sscgreen_v201806_grid201702_40d_'; % output file tag

T   = ncread(his_dir_f,'time');
Zts = ncread(his_dir_f,'ssh');
%convert time to days
T=squeeze(T)/(86400);

grd_dir = '/Users/rmueller/Data/SalishSeaCast/grid/';
grd_f = 'bathymetry_201702.nc';
grd_dir_f = fullfile(grd_dir,grd_f);

lat  = ncread(grd_dir_f,'nav_lat');
lon  = ncread(grd_dir_f,'nav_lon');
[x,y]= mapll(lat,lon,SLAT,SLON,HEMI); 
x = x-(min(x(:))); y = y-min(y(:));
h    = ncread(grd_dir_f,'Bathymetry');
% byte tmaskutil(t, y, x) ;
%   tmaskutil:standard_name = "tmaskutil" ;
%   tmaskutil:long_name = "dry land mask for T-grid and W-grid" ;
%   tmaskutil:flag_values = "0, 1" ;
%   tmaskutil:flag_meanings = "land, water" ;
mesh_dir = grd_dir;
mesh_f = 'mesh_mask201702.nc';
mesh_dir_f = fullfile(mesh_dir,mesh_f);
mask = ncread(mesh_dir_f,'tmaskutil');

cd(his_dir);

[L,M]=size(h);
% Lp = L - 1; Mp = M - 1;
% Lm = L - 2; Mm = M - 2;
% 
% lat_r = lat(2:Lp,2:Mp);
% lon_r = lon(2:Lp,2:Mp);
% mask_r = mask(2:Lp,2:Mp);

% if isfile('salishseacast_01012016_40d_TideAmpPh.mat')
%     display('*** Loading tide information *** ');
%     load('salishseacast_01012016_40d_TideAmpPh.mat')
% else
   display('*** Calculating tide information *** ');
    for j = 1:L;
        for l = 1:M
            for ci = 1:length(cons)
                tide_cons = char(cons(ci));
                % calculate amp/phase for each location of open ocean
                if mask(j,l)
                    [amp, ph]=esr_get_ap_mk3(squeeze(Zts(j,l,:)), T, tide_cons);
                    eval(['ssc_amp.' tide_cons '(j,l) = amp;'])
                    eval(['ssc_ph.' tide_cons '(j,l)  = ph;'])
                else
                    eval(['ssc_amp.' tide_cons '(j,l) = NaN;'])
                    eval(['ssc_ph.' tide_cons '(j,l)  = NaN;'])
                end
            end
        end
    end
%end

%% save results
display('*** Saving results *** ')
save([tag '_TideAmpPh'],'lon', 'lat', 'h','ssc_amp','ssc_ph');

display('*** Plotting tide amplitudes *** ');
for f_ind = 1:length(cons)
   
    tide_type = char(cons(f_ind))
    eval(['z = ssc_amp.' char(cons(f_ind)) ';']);
    
    figure(f_ind);
    pcolor(y,x,z);shading flat; hold on;
    colormap(cmocean('amp'));
    caxis([0 1.2])
    contour(y,x,mask,[0 1],'k');
    set(gca,'fontsize',fs);
    hc = colorbar('fontsize',fs);
    ylabel(hc,'elevation amplitude (m)')
    xlabel('distance (km)');
    ylabel('distance (km)');
    title([char(cons_fig(f_ind)) ' amplitude for SalishSeaCast-Green.v2018-06 '],'fontsize',fs);

    print('-dpng', '-r300',[tag '_amp_' char(cons_fig(f_ind))]); 

end

display('*** Plotting tide phases *** ');
for f_ind = 1:length(cons)
    eval(['z = ssc_ph.' char(cons(f_ind)) ';']);

    figure(f_ind+4);
    contourf(y,x,z,[0:20:360],'color',[0.3 0.3 0.3]);shading flat; hold on;
    caxis([0 360])
    hc = contourcmap('hsv',[0:20:360],'colorbar','on','Location','vertical')
    contour(y,x,mask,[0 1],'k');
    set(gca,'fontsize',fs);
    ylabel(hc,'phase (degrees)')
    xlabel('distance (km)');
    ylabel('distance (km)');
    title([char(cons_fig(f_ind)) ' phase for SalishSeaCast-Green.v2018-06 '],'fontsize',fs);

    print('-dpng', '-r300',[tag '_ph_' char(cons_fig(f_ind))]); 

end
