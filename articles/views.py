from django.views.generic import ListView, DetailView,  FormView
from django.views.generic.edit import UpdateView, DeleteView, CreateView 
from django.urls import reverse_lazy, reverse
from .models import Article, Comment
from .forms import CommentForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from api.serializers import ArticleSerializer

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"

class ArticleDetailView(LoginRequiredMixin, View):  
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleCreateView(LoginRequiredMixin, CreateView):  
    model = Article
    template_name = "article_new.html"
    fields = ("title", "body") 

    def form_valid(self, form):  
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  
    model = Article
    fields = (
        "title",
        "body",
        )
    template_name = "article_edit.html"

    def test_func(self):  
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):  
        obj = self.get_object()
        return obj.author == self.request.user
    
class CommentGet(DetailView):  
    model = Article
    template_name = "article_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context
    

class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.author = self.request.user
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class CommentEditView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment_edit.html"

    def get_queryset(self):
        # Ограничить доступ к редактированию только для автора комментария
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        # После редактирования вернуться к статье
        return reverse("article_detail", kwargs={"pk": self.object.article.pk})

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"
    
    def get_queryset(self):
        # Ограничить доступ к удалению только для автора комментария
        return Comment.objects.filter(author=self.request.user)
    
    def test_func(self):
        # Получаем объект комментария и статью, к которой он относится
        comment = self.get_object()
        article_author = comment.article.author
        # Проверка прав: текущий пользователь — автор комментария, администратор или автор статьи
        return (
            self.request.user == comment.author or
            self.request.user == article_author or
            self.request.user.is_staff
        )
    
    def get_success_url(self):
        # После удаления вернуться к статье
        return reverse("article_detail", kwargs={"pk": self.object.article.pk})

    
class ProtectedArticleListAPIView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]