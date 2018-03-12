% generate random rajectories for testing
%
% TODO: move to python
%       *just a quick Matlab solution for convenience*


function [] = generate_position_file(fileName,sourceID,N)

fs = 44100;

fs_ctl = 50;



fid = fopen(fileName,'w');

x = filter(ones(1,2000)/2000,1,randn(N,1))*15;

y = filter(ones(1,2000)/2000,1,randn(N,1))*15;

for IDX = 1:N
    
   fprintf(fid,'position \t'); 
   
   fprintf(fid,[num2str(IDX*fs/fs_ctl) '\t']);
   
   fprintf(fid,[num2str(sourceID) '\t']); 
   
   fprintf(fid,[num2str(x(IDX)) '\t']); 
   
   fprintf(fid,[num2str(y(IDX)) '\t']); 
   
   
   fprintf(fid,'\n');
       
end

fclose(fid);