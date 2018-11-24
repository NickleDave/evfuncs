%% make oracle data from test data (.cbin and associated .not.mat files)
cbins = dir('*.cbin');
for i = 1:length(cbins)
    cbin = cbins(i).name;
    cbin = fullfile(pwd, cbin);
    [dat, Fs, DOFILT, ext] = ReadDataFile(cbin, '0');
    % note that DOFILT gets set to 1 i.e. True by ReadDataFile for .cbins
    filter_type = 'hanningfir';   % what ReadDataFile sets for call to bandpass_filtfilt
    [filtsong] = bandpass_filtfilt(dat,Fs,500.0,10000.0,filter_type);
    save(strcat(cbin,'_filtsong.mat'), 'filtsong')
    [sm,sp,t,f] = SmoothData(dat,Fs,DOFILT);
    save(strcat(cbin,'_smooth_data.mat'), 'sm')
end