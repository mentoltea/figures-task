#include "nlist.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*typedef enum {
    false=0,
    true=1
} bool;
*/

typedef struct {
    int x, y;
} square;
LIST_DEF(square)


typedef struct {
    list_square* list;
} figure;
LIST_DEF(figure)

LIST_DEF(int)


char* itoa(int decimal) {
    if (decimal==0) {
        char* result = (char*)malloc(1*sizeof(char));
        result[0] = '0';
        return result;
    }
    char* alf = "0123456789";
    int cop = decimal;
    int n=1;
    while (cop / 10 > 0) {
        n += 1;
        cop /= 10;
    }
    char *result = (char*)malloc((n+1)*sizeof(char));
    result[n] = '\0';
    int last = 0;
    int end = n-1;
    while(decimal>0) {
        result[end] = alf[decimal%10];
        decimal /= 10;
        end--;
    }
    return result;
}



bool eq_int(int i1, int i2) {
    return i1==i2;
}

square add_square(square s, int vec[2]) {
    square ns = {s.x+vec[0], s.y+vec[1]};
    return ns;
}

bool eq_square(square s1, square s2) {
    if (s1.x == s2.x && s1.y == s2.y) {
        return true;
    }
    return false;
}

square copy_square(square s) {
    square ns = {s.x, s.y};
    return ns;
}

figure new_fig() {
    figure f;// = *((figure*) malloc(sizeof(figure)));
    f.list = NULL;
    return f;
}

void app_figure(figure *f, square s) {
    if (f->list==NULL) {
        f->list = new_square(s);
        return;
    }
    if (in_square(f->list, s, eq_square)) {
        return;
    }
    append_square(f->list, s);
}

figure copy_figure(figure f) {
    figure res;
    res.list = list_copy_square(f.list);
    return res;
}


figure add_figure(figure fig, int vec[2]) {
    figure f = copy_figure(fig);
    square temp;
    for (int n=0; n<len_square(f.list); n++) {
        temp = find_square(f.list, n);
        temp = add_square(temp, vec);
        replace_square(f.list, n, temp);
    }
    return f;
}

bool eq_figure(figure f1, figure f2) {
    if (len_square(f1.list) != len_square(f2.list)) {
        return false;
    }
    square temp;
    for (int i=0; i<f1.list->length; i++) {
        temp = find_square(f1.list, i);
        if (in_square(f2.list, temp, eq_square) == false) {
            return false;
        }
    }
    return true;
}

/*
figure rotate(figure fig) {
    figure f = copy_figure(f);
    if (!f.list) {
        return f;
    }
    
    print_figure(f);
    replace_square(f.list, 0, find_square(f.list, 0));
    printf("### %d\n", find_square(f.list, 0).x);
    return;
    square temp;
    for (int i=0; i<f.list->length; i++) {
        temp = find_square(f.list, i);
        int vec = {-temp.y-temp.x, -temp.y+temp.x};
        temp = add_square(temp, vec);
        replace_square(f.list, i, temp);
    }
    return f;
}
*/

void sortx(figure f, bool rev) {
    qsortx(f.list, 0, f.list->length-1);
    if (rev==true) {
        reverse_square(f.list);
    }
}

void sorty(figure f, bool rev) {
    qsorty(f.list, 0, f.list->length-1);
    if (rev==true) {
        reverse_square(f.list);
    }
}


int minx(figure f) {
    sortx(f, false);
    return f.list->val.x;
}

int maxx(figure f) {
    sortx(f, true);
    return f.list->val.x;
}

int miny(figure f) {
    sorty(f, false);
    return f.list->val.y;
}

int maxy(figure f) {
    sorty(f, true);
    return f.list->val.y;
}

bool suitnormalized(figure fig, figure plane) {
    if ((maxx(fig) > maxx(plane)) || (maxy(fig) > maxy(plane))) return false;

    for (int i=0; i<fig.list->length; i++) {
        square s = find_square(fig.list, i);
        if (!(in_square(plane.list, s, eq_square))) {
            int vec1[] = {1,0}; int vec2[] = {0,1};
            figure f1 = add_figure(fig, vec1);
            figure f2 = add_figure(fig, vec2);
            

            bool res = (suitnormalized(f1,plane) || suitnormalized(f2,plane));
            destroy_square(f1.list);free(f1.list);
            destroy_square(f2.list);free(f2.list);
            return res;
        }
    }
    return true;
}


bool suit(figure self, figure plane) {
    if (!self.list) {return true;}
    int smax = maxx(self); int smix = minx(self);
    int smay = maxy(self); int smiy = miny(self);

    int fmax = maxx(plane); int fmix = minx(plane);
    int fmay = maxy(plane); int fmiy = miny(plane);

    if ((smax-smix > fmax-fmix) || (smay-smiy > fmay-fmiy)) return false;

    int vec[] = {fmix-smix, fmiy-smiy};
    figure temp = add_figure(self, vec);
    bool res = suitnormalized(temp, plane);

    destroy_square(temp.list);free(temp.list);
    //destroy_square(self.list);
    return res;
}


void print_figure(figure f) {
    printf("\n{");
    if (!f.list) {
        printf("}\n"); return;
    }
    
    square temp;
    for (int i=0; i<f.list->length; i++) {
        temp = find_square(f.list, i);
        printf("(%d,%d), ", temp.x, temp.y);
    }
    printf("}\n");
}



void qsortx(list_square *list, int left, int right)
{
  int pivot; // разрешающий элемент
  int l_hold = left; //левая граница
  int r_hold = right; // правая граница
  //pivot = numbers[left];
  square pv = find_square(list, left);
  pivot = pv.x;
  while (left < right) // пока границы не сомкнутся
  {
        while ((find_square(list, right).x >= pivot) && (left < right))
            right--; // сдвигаем правую границу пока элемент [right] больше [pivot]
        if (left != right) // если границы не сомкнулись
        {
            replace_square(list, left, find_square(list, right));
            //numbers[left] = numbers[right]; // перемещаем элемент [right] на место разрешающего
            left++; // сдвигаем левую границу вправо
        }
        while ((find_square(list, left).x <= pivot) && (left < right))
            left++; // сдвигаем левую границу пока элемент [left] меньше [pivot]
        if (left != right) // если границы не сомкнулись
        {
            replace_square(list, right, find_square(list, left));
            //numbers[right] = numbers[left]; // перемещаем элемент [left] на место [right]
            right--; // сдвигаем правую границу влево
        }
  }
  replace_square(list, left, pv);
  //numbers[left] = pivot; // ставим разрешающий элемент на место
  pivot = left;
  left = l_hold;
  right = r_hold;
  if (left < pivot) // Рекурсивно вызываем сортировку для левой и правой части массива
        qsortx(list, left, pivot - 1);
  if (right > pivot)
        qsortx(list, pivot + 1, right);
}

void qsorty(list_square *list, int left, int right)
{
  int pivot; // разрешающий элемент
  int l_hold = left; //левая граница
  int r_hold = right; // правая граница
  //pivot = numbers[left];
  square pv = find_square(list, left);
  pivot = pv.y;
  while (left < right) // пока границы не сомкнутся
  {
        while ((find_square(list, right).y >= pivot) && (left < right))
            right--; // сдвигаем правую границу пока элемент [right] больше [pivot]
        if (left != right) // если границы не сомкнулись
        {
            replace_square(list, left, find_square(list, right));
            //numbers[left] = numbers[right]; // перемещаем элемент [right] на место разрешающего
            left++; // сдвигаем левую границу вправо
        }
        while ((find_square(list, left).y <= pivot) && (left < right))
            left++; // сдвигаем левую границу пока элемент [left] меньше [pivot]
        if (left != right) // если границы не сомкнулись
        {
            replace_square(list, right, find_square(list, left));
            //numbers[right] = numbers[left]; // перемещаем элемент [left] на место [right]
            right--; // сдвигаем правую границу влево
        }
  }
  replace_square(list, left, pv);
  //numbers[left] = pivot; // ставим разрешающий элемент на место
  pivot = left;
  left = l_hold;
  right = r_hold;
  if (left < pivot) // Рекурсивно вызываем сортировку для левой и правой части массива
        qsorty(list, left, pivot - 1);
  if (right > pivot)
        qsorty(list, pivot + 1, right);
}

void quicksort(list_int *list, int left, int right)
{
  int pivot; // разрешающий элемент
  int l_hold = left; //левая граница
  int r_hold = right; // правая граница
  //pivot = numbers[left];
  int pv = find_int(list, left);
  pivot = pv;
  while (left < right) // пока границы не сомкнутся
  {
        while ((find_int(list, right) >= pivot) && (left < right))
            right--; // сдвигаем правую границу пока элемент [right] больше [pivot]
        if (left != right) // если границы не сомкнулись
        {
            replace_int(list, left, find_int(list, right));
            //numbers[left] = numbers[right]; // перемещаем элемент [right] на место разрешающего
            left++; // сдвигаем левую границу вправо
        }
        while ((find_int(list, left) <= pivot) && (left < right))
            left++; // сдвигаем левую границу пока элемент [left] меньше [pivot]
        if (left != right) // если границы не сомкнулись
        {
            replace_int(list, right, find_int(list, left));
            //numbers[right] = numbers[left]; // перемещаем элемент [left] на место [right]
            right--; // сдвигаем правую границу влево
        }
  }
  replace_int(list, left, pv);
  //numbers[left] = pivot; // ставим разрешающий элемент на место
  pivot = left;
  left = l_hold;
  right = r_hold;
  if (left < pivot) // Рекурсивно вызываем сортировку для левой и правой части массива
        quicksort(list, left, pivot - 1);
  if (right > pivot)
        quicksort(list, pivot + 1, right);
}



list_figure *formfigures(figure fi, int k) {
    figure f = copy_figure(fi);

    list_figure *res = NULL;
    if (k==0) {
        res = new_figure(f);
        return res;
    }

    if (!f.list) { //==NULL
        square temp = {0,0};
        app_figure(&f, temp);
        res = formfigures(f, k-1);
        return res;
    }

    
    int vec1[] = {0,1}; int vec2[] = {1,0};
    int vec3[] = {0,-1}; int vec4[] = {-1,0};
    square s;
    list_square *potential = new_square(add_square(f.list->val, vec1));
    list_square *ptr = f.list;
    while (ptr) { //ptr!=NULL
        s = ptr->val;
        append_square(potential, add_square(copy_square(s), vec1));
        append_square(potential, add_square(copy_square(s), vec2));
        append_square(potential, add_square(copy_square(s), vec3));
        append_square(potential, add_square(copy_square(s), vec4));

        ptr = ptr->next;
    }


    int i = 0;
    int j;
    list_int *ignore = new_int(-1);
    ptr = potential;
    list_square *ptr2;
    figure fc;
    
    while (ptr) {
        if (in_int(ignore, i, eq_int)) {
            ptr = ptr->next; i++; continue;
        }
        ptr2 = ptr->next; j=i+1;
        while (ptr2) {
            if (eq_square(ptr->val, ptr2->val)) {
                append_int(ignore, j);
            }
            ptr2 = ptr2->next; j++;
        }
        s = ptr->val;

        if (!in_square(f.list, s, eq_square)) {
            figure fc = copy_figure(f);
            app_figure(&fc, s);
            if (res) {
                unit_figure(res, formfigures(fc, k-1));
            } else {
                res = formfigures(fc, k-1);
            }
            destroy_square(fc.list);free(fc.list);
        }

        ptr = ptr->next; i++;
    }

    destroy_square(potential); free(potential);
    destroy_square(f.list); free(f.list);
    destroy_int(ignore); free(ignore);
    ignore = new_int(-1);
    list_figure *fptr = res;
    list_figure *fptr2;
    i = 0;
    while (fptr) {
        if (in_int(ignore, i, eq_int)) {
            fptr = fptr->next; i++; continue;
        }
        fptr2 = fptr->next; j=i+1;
        while (fptr2) {
            if (eq_figure(fptr->val, fptr2->val)) {
                append_int(ignore, j);
            }
            fptr2 = fptr2->next; j++;
        }
        fptr = fptr->next; i++;
    }
    
    quicksort(ignore, 0, ignore->length-1);
    list_int *iptr = ignore;
    fptr = res;
    fptr2 = fptr;
    i = 0; j = 0;
    int p = 0;
    while (fptr) {
        if (in_int(ignore, i, eq_int)) {
            fptr = fptr->next; i++;
            free(fptr2->next);
            fptr2->next = fptr;
            res->length--;
            continue;    
        }
        fptr2 = fptr;
        fptr = fptr->next; i++;
    }
    destroy_int(ignore); free(ignore);
    return res;
}


void clear(list_figure* list) {
    list_figure* ptr = list;
    while (ptr) {
        if (ptr->val.list){
            destroy_square(ptr->val.list);free(ptr->val.list);
        }
        ptr = ptr->next;
    }
    destroy_figure(list); free(list);
}

int main() {
    int n = 9;
    figure f = new_fig();
    printf("forming planes for n=%d...\n", n);
    list_figure *plane = formfigures(f, n);
    printf("%d planes formed\n", len_figure(plane));
    float results[n+1];
    int local_suit = 0;
    int local_notsuit = 0;
    list_figure *temp, *ptr, *ptr2;

    for (int i=0; i<n+1; i++) {
        local_suit = 0;
        local_notsuit = 0;
        if (i==n) {
            temp = plane;
        } else {
            printf("forming for %d...\n", i);
            temp = formfigures(f,i); 
        }

        printf("%d figures formed for k=%d, linking...\n", temp->length, i);
        ptr = temp;
        while (ptr) {
            ptr2 = plane;
            while (ptr2) {
                if (suit(ptr->val, ptr2->val)) {
                    local_suit++;
                } else { local_notsuit++; }
                ptr2 = ptr2->next;
            }
            if (ptr->val.list && i!=n) {destroy_square(ptr->val.list); free(ptr->val.list); ptr->val.list=NULL;}
            ptr = ptr->next;
        }
        clear(temp);

        results[i] = (float)local_suit/(float)(local_suit+local_notsuit);
        printf("#####\nchance is %f for %d\n\n", results[i], i);
    }

    //clear(plane);
    
    char* nstr = itoa(n);
    char* filename = (char*)malloc((5+strlen(nstr)+3)*sizeof(char));
    memcpy(filename, "../", 3*sizeof(char));
    memcpy(filename+3, nstr, strlen(nstr)*sizeof(char));
    memcpy(filename+strlen(nstr)+3, ".txt\0", 5*sizeof(char));
    //printf("%s\n", filename);
    FILE* file = fopen(filename, "w");
    if (!file) {
        printf("Cant open file %s\n", filename);
        exit(1);
    }

    for (int i=0; i<n+1; i++) {
        fprintf(file, "%d %f\n", i, results[i]);
    }

    fclose(file);
    free(nstr);
    free(filename);
    
    return 0;
}