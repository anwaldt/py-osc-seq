

function [] = mirror_x(fileName,outName,newID)



fid = fopen(fileName);

X = textscan(fid,'%s %f %d %f%f');

fclose(fid);

X{4} = X{4}*-1;

N = length(X{4});

fid = fopen(outName,'w');



for IDX = 1:N
    
   fprintf(fid,'position \t'); 
   
   fprintf(fid,[num2str(X{2}(IDX)) '\t']);
   
   fprintf(fid,[num2str(newID) '\t']); 
   
   fprintf(fid,[num2str(X{4}(IDX)) '\t']); 
   
   fprintf(fid,[num2str(X{5}(IDX)) '\t']); 
   
   
   fprintf(fid,'\n');
       
end