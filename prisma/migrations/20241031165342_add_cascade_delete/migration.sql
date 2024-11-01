-- DropForeignKey
ALTER TABLE "comment" DROP CONSTRAINT "comment_article_id_fkey";

-- DropForeignKey
ALTER TABLE "like" DROP CONSTRAINT "like_article_id_fkey";

-- AddForeignKey
ALTER TABLE "comment" ADD CONSTRAINT "comment_article_id_fkey" FOREIGN KEY ("article_id") REFERENCES "article"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "like" ADD CONSTRAINT "like_article_id_fkey" FOREIGN KEY ("article_id") REFERENCES "article"("id") ON DELETE CASCADE ON UPDATE CASCADE;
