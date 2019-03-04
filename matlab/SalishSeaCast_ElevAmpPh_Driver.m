close all; clear all;
out_dir = pwd;

%define paths
if strcmp(computer,'GLNXA64');
    path(path,'/home/rmueller/toolbox/matlab/tides//PlotTideAmpPhase');
    path(path,'/home/rmueller/toolbox/matlab/tides/TMD_2.01/FUNCTIONS');
    path(path, fullfile('/home/rmueller/toolbox/matlab/colormaps/cmocean_v1/cmocean'))
    
    grd_dir = '/home/rmueller/Data/SalishSeaCast/grid/';
    grd_f = 'bathymetry_201702.nc';
    grd_dir_f = fullfile(grd_dir,grd_f);
    
    out_dir = '/home/rmueller/Projects/MIDOSS/analysis-rachael/matlab';
    
    hdr.t = 'time in format "seconds since 1900-01-01 00:00:00" ';
    hdr.Zts = 'SSH in format of meters above geoid with NAN values = 1e20f.';
    hdr.source = '/results2/SalishSea/nowcast-green.201806/';
    hdr.date = date;
    hdr.created_by = 'Rachael D. Mueller';
   
else   
    
    path(path,'/Users/rmueller/toolbox/matlab/ROMS/Tides/PlotTideAmpPhase');
    path(path,'/Users/rmueller/toolbox/matlab/TMD_2.01/FUNCTIONS');
    path(path, fullfile('/Users/rmueller/toolbox/matlab/Colormaps/cmocean_v1/cmocean'))
 
    his_dir = '/Users/rmueller/Projects/MIDOSS/analysis-rachael/matlab/';
    his_ssh = 'ubcSSgSurfaceTracerFields1hV18-06_01012019_40day.nc';
    his_dir_f = fullfile(his_dir, his_ssh);
        
    out_dir = his_dir;
    
    %define grid location
    grd_dir = '/Users/rmueller/Data/SalishSeaCast/grid/';
    grd_f = 'bathymetry_201702.nc';
    grd_dir_f = fullfile(grd_dir,grd_f);
    
    %define header information
    hdr.t = 'time in format "seconds since 1900-01-01 00:00:00" ';
    hdr.Zts = 'SSH in format of meters above geoid with NAN values = 1e20f.';
    hdr.source = '/results2/SalishSea/nowcast-green.201806/';
    hdr.date = date;
    hdr.created_by = 'Rachael D. Mueller';    
end

cons = {'m2', 's2', 'k1', 'o1','mk3','m4', 'n2','p1','k2','q1'};
cons_fig = {'M_2','S_2','K_1','O_1','MK_3','M_4', 'N_2','P_1','K_2','Q_1'};
%cons = {'n2  ';'p1  ';'k2  ';'q1  '};
%cons_fig = {'N_2','P_1','K_2','Q_1'};

% load bathymetry and convert to polar stereographic projection
SLAT = '70';SLON = -20; HEMI = 'n';
lat  = ncread(grd_dir_f,'nav_lat');
lon  = ncread(grd_dir_f,'nav_lon');
[x,y]= mapll(lat,lon,SLAT,SLON,HEMI);
x = x-(min(x(:))); y = y-min(y(:));
mesh_dir = grd_dir;
mesh_f = 'mesh_mask201702.nc';
mesh_dir_f = fullfile(mesh_dir,mesh_f);
mask = ncread(mesh_dir_f,'tmaskutil');

%specify for graphic
fs = 12;


% set initial date and number of days for analysis
start_date = datenum(2016,01,01);
ndays = 90;
monthstr = {'jan','feb','mar','apr'};
% Save first day for t_ind=1 to use in output file name
firstday = datevec(start_date);
firstday_str = [num2str(firstday(1)) num2str(firstday(2),'%02.f') num2str(firstday(3),'%02.f')];

% set name of output ssh file
ssh_mat = ['SalishSea_1h_SSH_' firstday_str  '_' num2str(ndays) 'd'];
amph_mat = ['SalishSea_1h_SSH_' firstday_str  '_' num2str(ndays) 'd_TideAmpPh']; 
graphic_tag = ['SalishSea_1h_SSH_' firstday_str  '_' num2str(ndays) 'd_TideAmpPh']; %used for output graphic filenames

% check to see if SSH .mat file exists and create it if it doesn't
if exist(fullfile(out_dir,[ssh_mat '.mat']))
    display(['*** Loading SSH .mat file ***']);
    load(fullfile(out_dir,ssh_mat))
else
    % 48hrs of SSH (m) starting from 01/01/2016, OO:30:00Z
    if strcmp(computer,'GLNXA64');
        his_dir = '/results2/SalishSea/nowcast-green.201806/';
        %loop over 120 days (ndays) and concatenate output
        tstart = tic;
        % Read in data over "ndays" and concatenate SSH
        for t_ind = 1:ndays
            loopstart = tic;
            % Directory named by date. Define date and move to that directory.
            dvec = datevec(start_date + t_ind-1);
            dir_str = [his_dir num2str(dvec(3),'%02.f') char(monthstr(dvec(2))) '16'];
            cd(dir_str);
            % Create a filename string based on date and read in SSH (sossheig)
            date_str = [num2str(dvec(1)) num2str(dvec(2),'%02.f') num2str(dvec(3),'%02.f')];
            f_str   = ['SalishSea_1h_' date_str '_' date_str '_grid_T.nc'];
            % load SSH in format of meters above geoid with NAN values = 1e20f.
            ssh_in = ncread(fullfile(dir_str,f_str),'sossheig');
            %load time in format "seconds since 1900-01-01 00:00:00"
            time_in= ncread(fullfile(dir_str,f_str), 'time_centered');
            % Concatenate SSH after first time step
            if t_ind == 1
                Zts = ssh_in;
                T = time_in;
            else
                Zts = cat(3, Zts, ssh_in);
                T = cat(1, T, time_in);
            end
            if rem(t_ind,10)==0
                display(['Day ' num2str(t_ind) ' of ' num2str(ndays) ', ' num2str(toc(loopstart), '%5.2f') ' s.' ])
            end
        end
        t_end = toc(tstart);
        display(['total loop time: ' num2str(t_end) ' s']);
        
        %save model output to file
        hdr.firstday = firstday_str;
        hdr.ndays = ndays;
        save(fullfile(out_dir,ssh_mat), 'Zts','T','hdr','-v7.3');
        
    else % Macbook pro
        T   = ncread(his_dir_f,'time');
        Zts = ncread(his_dir_f,'ssh');
        %convert time to days
        T=squeeze(T)/(86400);
    end   
end

if exist(fullfile(out_dir, [amph_mat '.mat']))
    display(['*** Loading amplitude and phase .mat file ***']);
    load(fullfile( out_dir, amph_mat))
else
    h    = ncread(grd_dir_f,'Bathymetry');
    % byte tmaskutil(t, y, x) ;
    %   tmaskutil:standard_name = "tmaskutil" ;
    %   tmaskutil:long_name = "dry land mask for T-grid and W-grid" ;
    %   tmaskutil:flag_values = "0, 1" ;
    %   tmaskutil:flag_meanings = "land, water" ;
    
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
        display(['finished with collumn ' num2str(j)]);
    end
    %end
    
    %% save results
    display('*** Saving results *** ')
    save(fullfile(out_dir, amph_mat),'lon', 'lat', 'h','ssc_amp','ssc_ph');
end

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
    
    print('-dpng', '-r300',[graphic_tag '_amp_' char(cons_fig(f_ind))]);
    
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
    
    print('-dpng', '-r300',[graphic_tag '_ph_' char(cons_fig(f_ind))]);
    
end
