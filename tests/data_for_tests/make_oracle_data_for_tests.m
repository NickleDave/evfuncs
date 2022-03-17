%% make oracle data from test data (.cbin and associated .not.mat files)
% "oracle data" meaning 'data from the function whose output we need to match'
cbins = dir('*.cbin');
for i = 1:length(cbins)
    cbin = cbins(i).name;
    cbin = fullfile(pwd, cbin);
    [dat, Fs, DOFILT, ext] = ReadDataFile(cbin, '0');
    % note that DOFILT gets set to 1 i.e. True by ReadDataFile for .cbins
    filter_type = 'hanningfir';   % what ReadDataFile sets for call to bandpass_filtfilt
    % get bandpass_filtfilt output as oracle data to test evfuncs.bandpass_filtfilt
    [filtsong] = bandpass_filtfilt(dat,Fs,500.0,10000.0,filter_type);
    save(strcat(cbin,'_filtsong.mat'), 'filtsong')
    % get SmoothData output as oracle data to test evfuncs.smooth_data
    [sm,sp,t,f] = SmoothData(dat,Fs,DOFILT);
    save(strcat(cbin,'_smooth_data.mat'), 'sm')
    notmat = load(strcat(cbin,'.not.mat'));
    % get SegementNotes output as oracle data to test evfuncs.segment_song;
    % can't just use .not.mat files because user may have edited onsets
    % and/or offsets, and this will results in false errors
    [onsets, offsets]=SegmentNotes(sm, notmat.Fs, notmat.min_int, notmat.min_dur, notmat.threshold);
    save(strcat(cbin,'_unedited_SegmentNotes_output.mat'), 'onsets', 'offsets')
end